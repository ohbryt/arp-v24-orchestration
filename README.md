# ARP v24 Orchestration System
## Enhanced with v25 Agentic Framework

**Version:** 24.5 (Enhanced)  
**Updated:** 2026-05-01  
**GitHub:** https://github.com/ohbryt/arp-v24-orchestration

---

## Overview

This repository contains the **ARP v24 Orchestration System** - the task routing and multi-tool coordination layer for biomedical research. Enhanced with v25 agentic framework features.

### Key Components

| Component | Description |
|-----------|-------------|
| **Director Agent** | Task decomposition and routing (MiniMax-M2.7) |
| **Tool Registry** | 7 tools with intelligent fallback |
| **Cache Layer** | LLM response caching (TTL 24h) |
| **Provenance Tracker** | Reproducibility tracking |

### v25 Enhancements Added

| Enhancement | Status |
|-------------|--------|
| HypothesisAgent | ✅ Added |
| ExperimentAgent | ✅ Added |
| SelfHealingHarness | ✅ Added |
| Agentic Framework | ✅ Added |
| Tests (pytest) | ✅ Added |
| GitHub Actions CI | ✅ Added |

---

## Architecture

```
┌─────────────────────────────────────────┐
│         DIRECTOR AGENT                   │
│      (MiniMax-M2.7 Leader)              │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┼────────────┐
    ↓            ↓            ↓
┌────────┐  ┌────────┐  ┌────────┐
│ ROUTER │  │ CACHE  │  │PROVENANCE│
└────────┘  └────────┘  └─────────┘
                 │
                 ↓
┌─────────────────────────────────────────┐
│          TOOL REGISTRY                   │
│  ARP_PIPELINE | GROQ_LLAMA | CHEMBL    │
│  PUBMED | OLLAMA_GLM | OLLAMA_QWEN     │
└─────────────────────────────────────────┘
```

---

## v25 Agentic Features

### HypothesisAgent
```python
from arp_v25.agents.hypothesis_agent import HypothesisAgent

agent = HypothesisAgent()
hypotheses = await agent.generate(
    target="KDM4A",
    disease="lung_cancer",
    num_hypotheses=3
)
```

### ExperimentAgent
```python
from arp_v25.agents.experiment_agent import ExperimentAgent

agent = ExperimentAgent()
protocol = await agent.design(hypothesis=hypothesis)
```

### SelfHealingHarness
```python
from arp_v25.core.self_healing.harness import SelfHealingHarness

harness = SelfHealingHarness()
result = await harness.run(pipeline_task)
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Usage

```bash
# Run orchestration
python -m arp_v24.orchestration

# Run tests
pytest tests/ -v

# Lint
ruff check .
```

---

## Phase Status

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Tool Registry | ✅ Complete |
| Phase 2 | Director/Router | ✅ Complete |
| Phase 3 | Cache/Provenance | ✅ Complete |
| Phase 4 | Agentic Framework | ✅ Complete |

---

## Documentation

| Document | Description |
|----------|-------------|
| [ORCHESTRATION_SYSTEM_REPORT.md](./ORCHESTRATION_SYSTEM_REPORT.md) | Full system report |
| [ARP_V24_ARCHITECTURE_BLUEPRINT.md](./ARP_V24_ARCHITECTURE_BLUEPRINT.md) | Architecture details |
| [ARP_V24_IMPLEMENTATION_ROADMAP.md](./ARP_V24_IMPLEMENTATION_ROADMAP.md) | Implementation plan |

---

*Maintained by: ARP Research Team*  
*Last Updated: 2026-05-01*
