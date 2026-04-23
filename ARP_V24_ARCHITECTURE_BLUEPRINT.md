# ARP v24 - Pipeline Architecture Blueprint
## From Multi-Tool Integration to Optimal Research Pipeline

**Date:** 2026-04-23  
**Purpose:** Define the optimal architecture for our biomedical research pipeline  
**Status:** Draft v1 - Needs Review & Refinement  

---

## 1. Current State Assessment

### 1.1 What We Have Built

```
arp-v24/
├── core/
│   ├── scoring_engine.py      # Engine 1: Target Priority
│   ├── modality_routing.py   # Engine 2: Modality Router
│   ├── candidate_engine.py   # Engine 3: Candidate Ranker
│   └── schema.py             # Data models
├── api/
│   ├── chembl.py             # ChemBL API wrapper
│   └── pubmed.py             # PubMed API wrapper
├── integration/
│   ├── groq_client.py        # Groq LLM (Llama 3.3 70B)
│   ├── biocontext_mcp.py     # BioContext MCP
│   ├── diamond_deepclust.py  # Diamond DeepClust
│   └── ... (12+ integrations)
├── LinkLlama/                # Protein linker design
├── pipette_benchmark/        # Multi-agent bioinformatics
├── literature/               # Literature reports
└── skills/                   # ARP research skills
```

### 1.2 External Tools Available

| Category | Tool | Status | Speed |
|----------|------|--------|-------|
| **LLM (Fast)** | Groq (Llama 3.3 70B) | ✅ | ~0.6s |
| **LLM (Local)** | GLM-4.7-flash (30B) | ✅ | ~3.5s |
| **LLM (Local)** | Qwen3:14b | ✅ | ~13s |
| **LLM (Local)** | Qwen3:8b | ✅ | ~4s |
| **LLM (Local)** | Clinic-Copilot (14B) | ✅ | - |
| **Database** | ChemBL API | ✅ | ~2s |
| **Database** | PubMed API | ✅ | ~2s |
| **Structure** | AlphaFold3 | ⚠️ | External |
| **Docking** | RosettaSearch | ⚠️ | External |
| **Linker** | LinkLlama | ✅ | Local |

### 1.3 Problems Identified

1. **No unified orchestration** - Tools called individually, not as pipeline
2. **Inconsistent APIs** - Each tool has different interface
3. **No error recovery** - Failed steps don't trigger retry/alternative
4. **No caching** - Same queries repeated waste resources
5. **Manual routing** - Task → Tool assignment done manually
6. **No provenance tracking** - Can't trace which tool produced which result

---

## 2. Proposed Architecture

### 2.1 Layered Design

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│         (User Interface / Report Generation)                 │
├─────────────────────────────────────────────────────────────┤
│                    ORCHESTRATION LAYER                       │
│    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│    │  Director   │  │  Planner    │  │  Validator  │        │
│    │   Agent     │  │   Agent     │  │   Agent     │        │
│    └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────┤
│                     ROUTING LAYER                           │
│         (Task → Tool matching & load balancing)              │
├─────────────────────────────────────────────────────────────┤
│                    TOOL LAYER                               │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐    │
│  │Groq  │ │GLM   │ │Qwen  │ │ChemBL│ │PubMed│ │Local │    │
│  │      │ │4.7   │ │3:14b │ │      │ │      │ │Files │    │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘    │
├─────────────────────────────────────────────────────────────┤
│                    DATA LAYER                              │
│    (Cache, Memory, Provenance, Results Store)                │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Core Agents

| Agent | Role | Inputs | Outputs |
|-------|------|--------|---------|
| **Director** | Main orchestrator | Disease + Research Question | Execution Plan |
| **Planner** | Task decomposition | Goal | Sub-tasks + Tool assignments |
| **Executor** | Tool execution | Task + Tool | Result + Provenance |
| **Validator** | Quality control | Result + Criteria | Pass/Fail + Suggestions |
| **Synthesizer** | Report generation | All results | Final Report |

### 2.3 Tool Routing Logic

```python
def route_task(task, context):
    """Route task to optimal tool based on characteristics"""
    
    if task.type == "literature_search":
        if task.speed_required:
            return "Groq"  # Fast external
        elif task.complexity > THRESHOLD:
            return "PubMed"  # Direct API for complex
        else:
            return "Ollama:Qwen3:14b"  # Local fallback
            
    elif task.type == "code_generation":
        if task.complexity > HIGH:
            return "Ollama:Qwen3:14b"  # SWE-bench optimized
        else:
            return "Ollama:Qwen3:8b"  # Quick tasks
            
    elif task.type == "complex_reasoning":
        return "Ollama:GLM-4.7-flash"  # 30B for reasoning
        
    elif task.type == "bioactivity_data":
        return "ChemBL:API"  # Direct database
        
    elif task.type == "protein_structure":
        return "AlphaFold3:External"  # External service
```

---

## 3. Execution Flow

### 3.1 Research Request Flow

```
1. User Input
   "Sarcopenia에 대한 drug discovery 리포트 작성해줘"
   
2. Director Agent
   ↓
   ├── Disease: Sarcopenia
   ├── Goal: Drug discovery report
   ├── Constraints: Time < 5min, Accuracy > 80%
   └── Output: Execution Plan
   
3. Planner Agent
   ↓
   ├── Tasks:
   │   1. Target identification (Engine 1-3)
   │   2. Literature search (Groq + PubMed)
   │   3. Bioactivity data (ChemBL)
   │   4. Analysis (LLM)
   │   5. Report generation
   └── Tool assignments created
   
4. Parallel Execution
   ↓
   ┌─────────────────────────────────┐
   │ Task 1: ARP Pipeline (parallel) │
   │ Task 2: Literature (Groq)       │ ← Groq (0.6s)
   │ Task 3: ChemBL (parallel)       │
   └─────────────────────────────────┘
   
5. Validator Agent
   ↓
   ├── Quality checks
   │   ├── Target relevance > 0.5
   │   ├── Literature coverage > 80%
   │   └── Data freshness < 30 days
   └── Fail → Retry or Alternative path
   
6. Synthesizer Agent
   ↓
   Final Report (Markdown/PDF)
```

### 3.2 Tool Selection Matrix

| Task Type | Primary | Secondary | Tertiary |
|-----------|---------|-----------|----------|
| **Fast summarization** | Groq (0.6s) | Qwen3:14b (13s) | GLM-4.7 (3.5s) |
| **Literature analysis** | Groq | PubMed direct | - |
| **Code generation** | Qwen3:14b (SWE-bench 73%) | Qwen3:8b | - |
| **Complex reasoning** | GLM-4.7-flash (30B) | Groq | - |
| **Bioactivity data** | ChemBL API | ChEMBL direct | Manual |
| **Protein design** | LinkLlama | RosettaSearch | AlphaFold3 |
| **Docking** | Pipette | RosettaSearch | AutoDock-GPU |

---

## 4. Data Flow & Caching

### 4.1 Cache Strategy

```
Request → Cache Check → Cache Hit? → Return cached
                            ↓ No
                      Execute Tool → Store in Cache → Return
```

**Cache Categories:**
- **Literature:** TTL = 7 days (fast-moving field)
- **Bioactivity:** TTL = 30 days (stable data)
- **LLM responses:** TTL = 1 day (context-dependent)
- **Structures:** TTL = 90 days (stable)

### 4.2 Provenance Tracking

```json
{
  "result_id": "abc123",
  "task": "target_prioritization",
  "tool": "scoring_engine.py",
  "input": {...},
  "output": {...},
  "timestamp": "2026-04-23T08:00:00Z",
  "duration_ms": 450,
  "cache_hit": false,
  "dependencies": ["previous_result_xyz"]
}
```

---

## 5. Error Recovery

### 5.1 Failure Modes & Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| **Groq timeout** | > 5s | Switch to Ollama:Qwen3:14b |
| **ChemBL rate limit** | 429 response | Wait + retry with backoff |
| **LLM hallucination** | Validator fail | Re-run with stricter prompt |
| **Network failure** | Connection error | Use cached data + flag stale |
| **Out of memory** | OOM error | Reduce model size (8B → 4B) |

### 5.2 Circuit Breaker Pattern

```python
def call_with_circuit_breaker(tool, task, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = tool.execute(task)
            reset_circuit(tool)
            return result
        except TransientError as e:
            increment_failure(tool)
            if is_circuit_open(tool):
                return fallback_tool(task)
            wait(exponential_backoff(attempt))
        except PermanentError as e:
            return fallback_tool(task)
```

---

## 6. Implementation Priorities

### Phase 1: Core Infrastructure (This Week)
- [ ] Unify orchestration interface
- [ ] Implement cache layer
- [ ] Add provenance tracking
- [ ] Basic error recovery

### Phase 2: Tool Integration (Next Week)
- [ ] All existing tools wrapped with standard interface
- [ ] Tool selection logic implemented
- [ ] Parallel execution support

### Phase 3: Intelligence (Month 2)
- [ ] Learn from user feedback
- [ ] Optimize tool selection based on success rate
- [ ] Predict task duration
- [ ] Auto-scale based on load

---

## 7. Key Decisions Needed

### Decision 1: Primary Orchestration Language
- **Option A:** Python (current, rich libraries)
- **Option B:** TypeScript (if MCP-first)
- **Option C:** Hybrid (Python core + TS for MCP)

### Decision 2: Cache Backend
- **Option A:** File-based (simple, no server)
- **Option B:** SQLite (structured, fast)
- **Option C:** Redis (distributed, needs setup)

### Decision 3: Deployment Model
- **Option A:** Local-only (privacy, speed)
- **Option B:** Cloud burst (scale, cost)
- **Option C:** Hybrid (local default, cloud fallback)

---

## 8. Reference Architecture (Target State)

```
┌─────────────────────────────────────────────────────────────┐
│                        USER                                  │
│                   (DRCMOH / 창명 오)                         │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    DIRECTOR AGENT                            │
│         (Main session - MiniMax-M2.7 / Groq)                │
│                                                              │
│   Responsibilities:                                          │
│   - Parse user intent                                        │
│   - Create execution plan                                    │
│   - Orchestrate sub-agents                                   │
│   - Quality check final output                               │
└─────────────────────────┬───────────────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  RESEARCHER  │  │   CODER     │  │  ANALYST     │
│  (Sub-agent) │  │  (Sub-agent)│  │  (Sub-agent) │
│              │  │              │  │              │
│ - Literature │  │ - Python     │  │ - Data       │
│ - ChemBL     │  │ - Scripts    │  │ - Stats      │
│ - PubMed     │  │ - Debug      │  │ - Viz        │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     TOOL LAYER                               │
│                                                              │
│   Fast Tier:          Heavy Tier:         Data Tier:        │
│   ┌────────┐          ┌────────┐          ┌────────┐        │
│   │ Groq   │           │GLM-4.7 │          │ ChemBL │        │
│   │ 0.6s  │           │  30B  │          │  API   │        │
│   └────────┘          └────────┘          └────────┘        │
│   ┌────────┐          ┌────────┐          ┌────────┐        │
│   │Qwen3:  │           │Qwen3:  │          │ PubMed │        │
│   │  14b   │           │  8b    │          │  API   │        │
│   └────────┘          └────────┘          └────────┘        │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATA LAYER                               │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│   │ Cache   │  │Memory   │  │Results  │  │Provenanc│        │
│   │ (TTL)   │  │(Context)│  │(Store)  │  │(Trace)  │        │
│   └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
└─────────────────────────────────────────────────────────────┘
```

---

## 9. Next Steps

1. **Review this document** - Validate architecture decisions
2. **Prioritize implementation** - What gives most value first
3. **Allocate resources** - Time + compute budget
4. **Define success metrics** - How do we know it's working

---

*Document: ARP v24 Architecture Blueprint v1*  
*Created: 2026-04-23*  
*Author: OCM AI Assistant*