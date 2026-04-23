# ARP v24 - Implementation Roadmap
## From Current State to Optimal Pipeline

**Date:** 2026-04-23  
**Based on:** `ARP_V24_ARCHITECTURE_BLUEPRINT.md`  
**Status:** Draft for Review  

---

## Executive Summary

We have built substantial infrastructure across 23+ days of development:
- **9 target identification engines** (ARP v24 Engine 1-3)
- **12+ tool integrations** (Groq, ChemBL, PubMed, etc.)
- **4 local LLM models** (GLM-4.7-flash, Qwen3:14b/8b, Clinic-Copilot)
- **2 specialized tools** (LinkLlama, Pipette benchmark)

**Gap:** These components work independently but lack unified orchestration.

**Goal:** Create an architecture that automatically routes tasks to optimal tools with error recovery, caching, and provenance.

---

## Current Pain Points

| Problem | Impact | Frequency |
|---------|--------|-----------|
| Manual tool selection | Time浪费 | Every request |
| No caching | Slow repeated queries | Daily |
| No error recovery | Failed pipelines | Weekly |
| Inconsistent output format | Manual formatting | Every report |
| No provenance | Can't trace results | When debugging |

---

## Implementation Phases

### Phase 0: Quick Wins (Today-Tomorrow)

#### 0.1 Standardize Tool Interface
```python
# Current: Each tool has different API
engine1.prioritize_targets(DiseaseType.SARCOPENIA)
client.chat.completions.create(...)
subprocess.run(['curl', ...])

# Target: Unified interface
class Tool:
    def execute(self, task: Task) -> Result
    def health_check(self) -> bool
    def get_capabilities(self) -> List[str]
```

#### 0.2 Add Simple Caching
```python
# Use file-based cache for LLM responses
# Key: hash(task + params)
# TTL: 24 hours for LLM, 7 days for literature
```

#### 0.3 Document Tool Routing Rules
```python
# Create routing_matrix.md
# Document which tool for which task
# No more manual selection
```

**Deliverables:**
- `tool_interface.py` - Unified tool base class
- `cache_layer.py` - Simple file-based cache
- `ROUTING_MATRIX.md` - Tool selection guide

**Time:** ~4 hours

---

### Phase 1: Core Orchestration (Week 1)

#### 1.1 Director Agent
```python
class DirectorAgent:
    def __init__(self):
        self.tools = ToolRegistry.get_all()
        self.cache = CacheLayer()
        self.provenance = ProvenanceTracker()
    
    def process(self, request: ResearchRequest) -> Report:
        plan = self.create_plan(request)
        results = self.execute_plan(plan)
        return self.synthesize(results)
```

#### 1.2 Planner Agent
```python
class PlannerAgent:
    def decompose(self, goal: str) -> List[Task]:
        # Use LLM to break down goal into tasks
        # Assign optimal tool to each task
        # Handle dependencies
```

#### 1.3 Executor with Error Recovery
```python
class Executor:
    def execute_with_retry(self, task: Task) -> Result:
        for attempt in range(MAX_RETRIES):
            try:
                return self.call_tool(task)
            except TransientError:
                self.wait_and_retry()
                continue
        return self.fallback(task)
```

**Deliverables:**
- `director.py` - Main orchestration
- `planner.py` - Task decomposition
- `executor.py` - Execution with retry
- `cache_layer.py` - Provenance tracking

**Time:** ~2 days

---

### Phase 2: Tool Integration (Week 2)

#### 2.1 Wrap All Existing Tools

| Tool | Wrapper | Status |
|------|---------|--------|
| Groq | `tool_groq.py` | New |
| ChemBL | `tool_chembl.py` | Refactor api/chembl.py |
| PubMed | `tool_pubmed.py` | Refactor api/pubmed.py |
| GLM-4.7-flash | `tool_ollama.py` | Generic Ollama wrapper |
| Qwen3:14b | `tool_ollama.py` | Same |
| ARP Pipeline | `tool_arp.py` | Wrap core engines |
| LinkLlama | `tool_linkllama.py` | New |
| Pipette | `tool_pipette.py` | New |

#### 2.2 Tool Registry
```python
class ToolRegistry:
    _tools = {}
    
    @classmethod
    def register(cls, tool: Tool):
        cls._tools[tool.name] = tool
    
    @classmethod
    def get(cls, name: str) -> Tool:
        return cls._tools.get(name)
    
    @classmethod
    def list_by_capability(cls, cap: str) -> List[Tool]:
        return [t for t in cls._tools.values() 
                if cap in t.capabilities]
```

#### 2.3 Routing Engine
```python
class Router:
    def route(self, task: Task, context: Context) -> Tool:
        # Score each tool for this task
        # Return highest scoring tool
        # Handle fallback chains
```

**Deliverables:**
- `tools/` directory with standardized wrappers
- `registry.py` - Tool registry
- `router.py` - Intelligent routing

**Time:** ~3 days

---

### Phase 3: Intelligence (Week 3-4)

#### 3.1 Learn from Feedback
```python
class FeedbackLearner:
    def record(self, task, tool, result, rating):
        # Store feedback
        # Update routing weights
        # Optimize for user preferences
```

#### 3.2 Performance Prediction
```python
def predict_duration(task: Task) -> timedelta:
    # Based on historical data
    # Adjust for complexity
    # Handle concurrent load
```

#### 3.3 Auto-scaling
```python
# If queue > threshold, burst to cloud
# If load low, reduce model sizes
```

**Deliverables:**
- `feedback.py` - Learning system
- `predictor.py` - Duration estimation
- `scaler.py` - Auto-scaling logic

**Time:** ~1 week

---

## Resource Requirements

| Phase | Time | Compute | Complexity |
|-------|------|---------|------------|
| Phase 0 | 4 hours | Low | Easy |
| Phase 1 | 2 days | Medium | Moderate |
| Phase 2 | 3 days | Medium | Moderate |
| Phase 3 | 1 week | High | Complex |

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Scope creep | Focus on core orchestration first |
| Tool wrapper complexity | Use generic base class, inherit |
| Cache invalidation | Conservative TTL, manual override |
| User resistance | Keep simple CLI, add complexity gradually |

---

## Success Metrics

| Metric | Target |
|--------|--------|
| **Time to generate report** | < 5 minutes (from scratch) |
| **Cache hit rate** | > 50% for repeated queries |
| **Error recovery success** | > 80% of failures recovered |
| **Tool utilization** | All tools used regularly |
| **User satisfaction** | Manual tool selection eliminated |

---

## Immediate Actions

### Today
1. [ ] Review `ARP_V24_ARCHITECTURE_BLUEPRINT.md`
2. [ ] Decide Phase 0 priorities
3. [ ] Start tool interface standardization

### This Week
1. [ ] Complete Phase 0 (quick wins)
2. [ ] Start Phase 1 (core orchestration)
3. [ ] Weekly review + adjust

---

## Appendix: Current Tool Inventory

```
arp-v24/
├── core/
│   ├── scoring_engine.py      # Engine 1: Target Priority
│   ├── modality_routing.py   # Engine 2: Modality Router  
│   ├── candidate_engine.py   # Engine 3: Candidate Ranker
│   └── schema.py             # Data models
├── api/
│   ├── chembl.py             # ChemBL API
│   └── pubmed.py             # PubMed API
├── integration/
│   ├── groq_client.py        # Groq LLM
│   ├── biocontext_mcp.py     # BioContext
│   ├── diamond_deepclust.py  # Diamond DeepClust
│   ├── drugblip_integration.py
│   ├── firecrawl_integration.py
│   └── ... (8 more)
├── LinkLlama/                # Protein linker design
├── pipette_benchmark/        # Multi-agent bioinformatics
└── skills/
    └── arp-research/         # ARP research skills

Ollama Models (Local):
├── glm-4.7-flash (30B)       # Complex reasoning
├── qwen3:14b                  # Code generation
├── qwen3:8b                   # Quick tasks
├── clinic-copilot (14B)       # Specialized
└── nomic-embed-text           # Embeddings

External Services:
├── Groq (Llama 3.3 70B)       # Fast LLM
├── ChemBL API                  # Bioactivity data
├── PubMed API                  # Literature
└── AlphaFold3 (indirect)      # Structure prediction
```

---

*Document: ARP v24 Implementation Roadmap*  
*Created: 2026-04-23*  
*Next Review: 2026-04-30*