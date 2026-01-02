# HACI on LangSmith: Complete Implementation Guide

> Build a production-ready Harness-Enhanced Agentic Collaborative Intelligence system using LangGraph and LangSmith

---

## Understanding the Technology Stack

Before diving in, it's important to understand where each component runs:

| Component | Where It Runs | What It Does |
|-----------|---------------|--------------|
| **Your HACI Code** | Local machine / your servers | Python code you write and deploy |
| **LangGraph** | Python library (runs locally) | Orchestrates agent workflows as stateful graphs |
| **LangSmith** | Cloud platform (smith.langchain.com) | Observability, tracing, evaluation, monitoring |
| **LLM APIs** | Cloud (Anthropic, OpenAI, etc.) | Provides AI reasoning capabilities |

**Key Concept:** You write Python code locally using LangGraph. When your code runs, it automatically sends traces to LangSmith's cloud platform via API. You then view those traces and analytics on the LangSmith website—but you never create files or run code on LangSmith itself.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     YOUR LOCAL DEVELOPMENT MACHINE                       │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │  Your Python Code (src/, tests/, config/)                       │   │
│   │  • Agent implementations                                        │   │
│   │  • LangGraph workflows                                          │   │
│   │  • Tool integrations                                            │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                     │
│                                    ▼                                     │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │  LangGraph Library (pip install langgraph)                      │   │
│   │  • Executes your agent graphs                                   │   │
│   │  • Manages state and checkpoints                                │   │
│   │  • Handles human-in-the-loop workflows                          │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                     │
└────────────────────────────────────┼─────────────────────────────────────┘
                                     │ API calls (automatic)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        CLOUD SERVICES                                    │
│                                                                         │
│   ┌─────────────────────┐          ┌─────────────────────────────────┐  │
│   │  LangSmith Cloud    │          │  LLM Provider APIs              │  │
│   │  (Observability)    │          │  (Anthropic, OpenAI, etc.)      │  │
│   │  • View traces      │          │  • Claude, GPT-4, etc.          │  │
│   │  • Run evaluations  │          │  • Reasoning and generation     │  │
│   │  • Monitor costs    │          │                                 │  │
│   │  • Set up alerts    │          │                                 │  │
│   └─────────────────────┘          └─────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Table of Contents

1. [Setup & Prerequisites](#chapter-1-setup--prerequisites)
2. [Graph Architecture](#chapter-2-graph-architecture)
3. [Agent Implementation](#chapter-3-agent-implementation)
4. [Observability](#chapter-4-observability)
5. [Harness Phases Deep Dive](#chapter-5-harness-phases-deep-dive)
6. [Multi-Agent Swarm Coordination](#chapter-6-multi-agent-swarm-coordination)
7. [Context Engineering Integration](#chapter-7-context-engineering-integration)
8. [Human-in-the-Loop Patterns](#chapter-8-human-in-the-loop-patterns)
9. [Testing & Evaluation](#chapter-9-testing--evaluation)
10. [Production Deployment](#chapter-10-production-deployment)

---

## Chapter 1: Setup & Prerequisites

### Why LangSmith for HACI?

LangGraph provides the stateful, graph-based orchestration HACI needs for multi-agent coordination. LangSmith adds production-grade observability, evaluation, and debugging.

**LangGraph Benefits (runs locally as a Python library):**
- **Stateful Workflows:** Built-in persistence for long-running agent operations
- **Graph-Based Control:** Define agent interactions as nodes and edges
- **Human-in-the-Loop:** Native interrupt/resume for approval gates
- **Checkpointing:** Automatic state snapshots for recovery
- **Multi-Agent Patterns:** Supervisor, network, and hierarchical architectures

**LangSmith Benefits (cloud platform for observability):**
- **Deep Tracing:** Visualize every step of agent reasoning
- **Token Analytics:** Track costs per agent, per investigation
- **Evaluation Datasets:** Build test suites from production traces
- **Real-Time Monitoring:** Alerts for latency, errors, cost spikes
- **Prompt Management:** Version and A/B test system prompts

> **Perfect Fit for HACI:** HACI's THINK→ACT→OBSERVE→EVALUATE harness maps naturally to LangGraph nodes. Each phase becomes a node, the harness loop becomes a cycle in the graph, and multi-agent swarms become parallel branches that converge at a coordinator node.

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LANGSMITH CLOUD (Observability Dashboard)                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Tracing   │  │  Datasets   │  │ Evaluators  │  │  Monitoring │        │
│  │  (All Runs) │  │ (Test Data) │  │ (Accuracy)  │  │  (Alerts)   │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
└─────────┼────────────────┼────────────────┼────────────────┼────────────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│               LANGGRAPH EXECUTION (Runs on Your Infrastructure)             │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    HACI HARNESS GRAPH                               │   │
│   │                                                                     │   │
│   │    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    │   │
│   │    │  THINK   │───▶│   ACT    │───▶│ OBSERVE  │───▶│ EVALUATE │    │   │
│   │    │  Node    │    │  Node    │    │  Node    │    │   Node   │    │   │
│   │    └──────────┘    └──────────┘    └──────────┘    └────┬─────┘    │   │
│   │         ▲                                               │          │   │
│   │         │              ┌──────────────────┐              │          │   │
│   │         └──────────────│  CONTINUE/LOOP   │◀─────────────┘          │   │
│   │                        │  (Conditional)   │──────▶ COMPLETE/ESCALATE│   │
│   │                        └──────────────────┘                         │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    MULTI-AGENT SWARM GRAPH                          │   │
│   │   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   │   │
│   │   │  Log   │   │ Code   │   │ Infra  │   │  DB    │   │Security│   │   │
│   │   │ Agent  │   │ Agent  │   │ Agent  │   │ Agent  │   │ Agent  │   │   │
│   │   └───┬────┘   └───┬────┘   └───┬────┘   └───┬────┘   └───┬────┘   │   │
│   │       └────────────┴────────────┼────────────┴────────────┘        │   │
│   │                                 ▼                                   │   │
│   │                        ┌───────────────┐                            │   │
│   │                        │  COORDINATOR  │                            │   │
│   │                        │    (Swarm)    │                            │   │
│   │                        └───────────────┘                            │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              EXTERNAL SYSTEMS                               │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐         │
│   │  Jira   │  │ Datadog │  │ GitHub  │  │  Slack  │  │   AWS   │         │
│   │  (MCP)  │  │  (MCP)  │  │  (MCP)  │  │  (API)  │  │  (API)  │         │
│   └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Prerequisites

| Requirement | Details | Where | Status |
|-------------|---------|-------|--------|
| **LangSmith Account** | Sign up at smith.langchain.com. Free tier available for development. | Cloud (for observability) | Required |
| **Python 3.11+** | LangGraph requires Python 3.11 or higher for full async support. | Local machine | Required |
| **LLM API Keys** | Anthropic (Claude), OpenAI (GPT-4), or other supported providers. | Cloud APIs | Required |
| **Redis** | For context bus implementation (can use Docker locally). | Local or cloud | Optional |
| **PostgreSQL** | For LangGraph checkpointing and HACI's System of Record. | Local or cloud | Optional |
| **Docker** | For local development infrastructure and LangGraph Studio. | Local machine | Optional |

### Installation

#### Step 1: Create LangSmith Account (Cloud Setup)

Before writing any code, set up your LangSmith account:

1. **Go to** [smith.langchain.com](https://smith.langchain.com) and sign up
2. **Create a new project** called `haci-production` (or your preferred name)
3. **Generate an API key** from Settings → API Keys
4. **Save your API key** securely—you'll need it for the `.env` file

> **Note:** LangSmith is a cloud-based observability platform. You'll view traces, create datasets, and monitor performance through the web UI at smith.langchain.com. You don't install LangSmith locally—you install the `langsmith` Python package which sends data to the cloud.

#### Step 2: Create Local Project Directory

These commands run on **your local machine** (or development server) to create the project structure where you'll write your Python code:

```bash
# ═══════════════════════════════════════════════════════════════════════════
# LOCAL MACHINE COMMANDS
# These create directories on YOUR computer, NOT on LangSmith
# ═══════════════════════════════════════════════════════════════════════════

# Create project structure on your LOCAL MACHINE
mkdir haci-langsmith && cd haci-langsmith

# Create directory structure for your Python code
mkdir -p src/{agents,graphs,tools,memory,utils}
mkdir -p tests/{unit,integration,e2e}
mkdir -p config

# Initialize Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**What you just created locally:**
```
haci-langsmith/           # Your project root (LOCAL FILESYSTEM)
├── src/                  # Your Python source code
│   ├── agents/           # Agent implementations
│   ├── graphs/           # LangGraph workflow definitions
│   ├── tools/            # Tool integrations (Datadog, GitHub, etc.)
│   ├── memory/           # Context bus and checkpointing
│   └── utils/            # Shared utilities
├── tests/                # Test suites
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── config/               # Configuration files
└── venv/                 # Python virtual environment
```

#### Step 3: Install Python Dependencies (Local)

Create a `requirements.txt` file in your local project directory:

**requirements.txt:** (create this file on your local machine)
```txt
# ═══════════════════════════════════════════════════════════════════════════
# These are Python libraries that run on YOUR machine
# They connect to cloud services via API calls
# ═══════════════════════════════════════════════════════════════════════════

# Core LangChain ecosystem
langgraph>=0.2.0              # Runs LOCALLY - orchestrates agent workflows
langchain>=0.3.0              # Runs LOCALLY - LLM abstraction layer
langchain-anthropic>=0.2.0    # Runs LOCALLY - connects to Anthropic API
langchain-openai>=0.2.0       # Runs LOCALLY - connects to OpenAI API
langsmith>=0.1.0              # Runs LOCALLY - SENDS traces to LangSmith cloud

# LLM provider API clients
anthropic>=0.34.0             # Runs LOCALLY - calls Anthropic cloud API
openai>=1.50.0                # Runs LOCALLY - calls OpenAI cloud API

# State management
redis>=5.0.0                  # Connects to Redis (local Docker or cloud)
asyncpg>=0.29.0               # Connects to PostgreSQL (local or cloud)
psycopg2-binary>=2.9.0

# Utilities
pydantic>=2.0.0
python-dotenv>=1.0.0
structlog>=24.0.0
httpx>=0.27.0

# Testing
pytest>=8.0.0
pytest-asyncio>=0.23.0
```

Install the dependencies on your local machine:
```bash
# Run this command on your LOCAL machine in the project directory
pip install -r requirements.txt
```

#### Step 4: Configure Environment Variables (Local)

Create a `.env` file in your local project root. This file contains the API keys that connect your local code to cloud services:

**.env:** (create this file on your local machine—never commit to Git!)
```bash
# ═══════════════════════════════════════════════════════════════════════════
# LANGSMITH CONFIGURATION
# These settings tell your LOCAL code how to connect to LANGSMITH CLOUD
# ═══════════════════════════════════════════════════════════════════════════
LANGCHAIN_TRACING_V2=true                              # Enable sending traces to LangSmith
LANGCHAIN_API_KEY=lsv2_pt_xxxxxxxxxxxxxxxxxxxxxxxx     # Your LangSmith API key (from Step 1)
LANGCHAIN_PROJECT=haci-production                       # Project name in LangSmith
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com     # LangSmith API endpoint

# ═══════════════════════════════════════════════════════════════════════════
# LLM PROVIDER API KEYS
# These connect your LOCAL code to cloud LLM services
# ═══════════════════════════════════════════════════════════════════════════
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx      # From console.anthropic.com
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx             # From platform.openai.com (optional)

# ═══════════════════════════════════════════════════════════════════════════
# INFRASTRUCTURE (Optional - for production deployments)
# These can be local Docker containers or cloud-hosted services
# ═══════════════════════════════════════════════════════════════════════════
REDIS_URL=redis://localhost:6379/0                     # Local Redis or cloud Redis
DATABASE_URL=postgresql://user:pass@localhost:5432/haci  # Local or cloud PostgreSQL

# ═══════════════════════════════════════════════════════════════════════════
# HACI CONFIGURATION
# Application-specific settings (used by your local code)
# ═══════════════════════════════════════════════════════════════════════════
HACI_MAX_ITERATIONS=10
HACI_DEFAULT_CONFIDENCE_THRESHOLD=0.80
HACI_ENABLE_HUMAN_APPROVAL=true
```

#### Step 5: Verify Installation

Create this file on your local machine to verify everything is connected:

```python
# verify_setup.py (create this file in your LOCAL project root)
"""
Verification script to test that:
1. Local Python environment is configured
2. LangSmith cloud connection works
3. LangGraph library is installed
4. Environment variables are set correctly

This script runs LOCALLY and tests connections to CLOUD services.
"""

import os
from dotenv import load_dotenv

# Load environment variables from local .env file
load_dotenv()

def verify_setup():
    print("=" * 70)
    print("HACI + LangSmith Setup Verification")
    print("=" * 70)
    print("\nThis script runs on your LOCAL machine and tests cloud connections.\n")
    
    # Check environment variables
    print("1. Checking environment variables (from local .env file)...")
    langsmith_key = os.getenv("LANGCHAIN_API_KEY")
    if langsmith_key:
        print(f"   ✅ LANGCHAIN_API_KEY is set (ends with ...{langsmith_key[-4:]})")
    else:
        print("   ❌ LANGCHAIN_API_KEY not found in environment")
        print("      → Create a .env file with your LangSmith API key")
        return
    
    project = os.getenv("LANGCHAIN_PROJECT", "default")
    print(f"   ✅ Project name: {project}")
    
    tracing = os.getenv("LANGCHAIN_TRACING_V2")
    print(f"   ✅ Tracing enabled: {tracing}")
    
    # Test LangSmith cloud connection
    print("\n2. Testing LangSmith CLOUD connection...")
    try:
        from langsmith import Client
        client = Client()
        print(f"   ✅ Connected to LangSmith cloud: {client.api_url}")
        print(f"      → View traces at: https://smith.langchain.com")
    except Exception as e:
        print(f"   ❌ LangSmith connection failed: {e}")
        print(f"      → Check your LANGCHAIN_API_KEY in .env")
        return
    
    # Test LangGraph installation (local library)
    print("\n3. Testing LangGraph installation (LOCAL library)...")
    try:
        from langgraph.graph import StateGraph
        graph = StateGraph(dict)
        print("   ✅ LangGraph library is installed and working")
    except ImportError as e:
        print(f"   ❌ LangGraph not installed: {e}")
        print(f"      → Run: pip install langgraph")
        return
    
    # Test Anthropic API (optional)
    print("\n4. Checking LLM API keys...")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key:
        print(f"   ✅ ANTHROPIC_API_KEY is set (for Claude)")
    else:
        print("   ⚠️  ANTHROPIC_API_KEY not set (optional but recommended)")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print(f"   ✅ OPENAI_API_KEY is set (for GPT-4)")
    else:
        print("   ⚠️  OPENAI_API_KEY not set (optional)")
    
    print("\n" + "=" * 70)
    print("🎉 Setup complete! Ready to build HACI.")
    print("=" * 70)
    print("\n📍 Key points to remember:")
    print("   • Your code runs LOCALLY using LangGraph")
    print("   • Traces are automatically sent to LANGSMITH CLOUD")
    print("   • View traces at: https://smith.langchain.com")
    print("   • LLM calls go to ANTHROPIC/OPENAI cloud APIs")
    print("\n🚀 Next: Create your first agent in src/agents/")

if __name__ == "__main__":
    verify_setup()
```

Run the verification on your local machine:
```bash
# Run this on your LOCAL machine
python verify_setup.py
```

Expected output:
```
======================================================================
HACI + LangSmith Setup Verification
======================================================================

This script runs on your LOCAL machine and tests cloud connections.

1. Checking environment variables (from local .env file)...
   ✅ LANGCHAIN_API_KEY is set (ends with ...xxxx)
   ✅ Project name: haci-production
   ✅ Tracing enabled: true

2. Testing LangSmith CLOUD connection...
   ✅ Connected to LangSmith cloud: https://api.smith.langchain.com
      → View traces at: https://smith.langchain.com

3. Testing LangGraph installation (LOCAL library)...
   ✅ LangGraph library is installed and working

4. Checking LLM API keys...
   ✅ ANTHROPIC_API_KEY is set (for Claude)
   ⚠️  OPENAI_API_KEY not set (optional)

======================================================================
🎉 Setup complete! Ready to build HACI.
======================================================================

📍 Key points to remember:
   • Your code runs LOCALLY using LangGraph
   • Traces are automatically sent to LANGSMITH CLOUD
   • View traces at: https://smith.langchain.com
   • LLM calls go to ANTHROPIC/OPENAI cloud APIs

🚀 Next: Create your first agent in src/agents/
```

### Complete Project Structure

After setup, your **local** project directory should look like this:

```
haci-langsmith/                    # LOCAL: Your project root
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py          # Abstract agent interface
│   │   ├── log_agent.py           # Log analysis specialist
│   │   ├── code_agent.py          # Code analysis specialist
│   │   ├── infra_agent.py         # Infrastructure specialist
│   │   ├── db_agent.py            # Database specialist
│   │   └── security_agent.py      # Security specialist
│   ├── graphs/
│   │   ├── __init__.py
│   │   ├── harness_graph.py       # THINK→ACT→OBSERVE→EVALUATE
│   │   └── swarm_graph.py         # Multi-agent coordination
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── datadog_tools.py       # Monitoring tools
│   │   ├── github_tools.py        # Code repository tools
│   │   ├── jira_tools.py          # Issue tracking tools
│   │   └── aws_tools.py           # Cloud infrastructure tools
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── context_bus.py         # Redis-based context sharing
│   │   └── checkpointer.py        # PostgreSQL state persistence
│   └── utils/
│       ├── __init__.py
│       ├── prompts.py             # System prompts
│       └── config.py              # Configuration management
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── config/
│   └── settings.yaml
├── .env                           # API keys (DO NOT COMMIT TO GIT)
├── .gitignore                     # Include .env in this file!
├── requirements.txt
├── verify_setup.py
└── README.md
```

**Remember the distinction:**
- All code in this structure lives on **your local machine** (or your servers)
- When you run your code, the `langsmith` package automatically sends traces to **LangSmith cloud**
- You view results at **smith.langchain.com** in your browser

---

## Chapter 2: Graph Architecture

### State Schema Design

The HarnessState TypedDict defines all data that flows through the investigation graph. LangGraph uses this schema to track state across nodes and persist between runs.

> **Where this runs:** This is Python code that you create and run **locally** on your machine. LangGraph manages state in memory (or PostgreSQL for persistence). The `@traceable` decorator sends execution trace data to LangSmith cloud for observability.

```python
"""
HACI Harness State Schema

File: src/state/harness_state.py
Location: YOUR LOCAL MACHINE

This TypedDict defines the complete state structure for HACI investigations.
LangGraph uses this to track state across nodes and enable checkpointing.
"""

from typing import TypedDict, Annotated, Optional, List, Literal
from datetime import datetime
from pydantic import BaseModel, Field
import operator


# =============================================================================
# Pydantic Models for Structured Data
# =============================================================================

class Hypothesis(BaseModel):
    """A hypothesis about the root cause of an issue."""
    id: str = Field(..., description="Unique identifier for this hypothesis")
    description: str = Field(..., description="What we think might be wrong")
    confidence: float = Field(0.0, ge=0.0, le=1.0, description="Current confidence level")
    evidence_for: List[str] = Field(default_factory=list)
    evidence_against: List[str] = Field(default_factory=list)
    status: Literal["active", "confirmed", "rejected"] = "active"


class ToolCall(BaseModel):
    """Record of a tool invocation and its result."""
    tool_name: str
    arguments: dict
    result: Optional[str] = None
    error: Optional[str] = None
    duration_ms: int = 0
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class Observation(BaseModel):
    """An insight derived from tool results."""
    id: str
    source_tool: str
    finding: str
    relevance: float = Field(0.0, ge=0.0, le=1.0)
    supports_hypothesis: Optional[str] = None


class InvestigationStep(BaseModel):
    """A planned action in the investigation."""
    tool: str
    purpose: str
    arguments: dict
    priority: int = 1


# =============================================================================
# Main State TypedDict
# =============================================================================

class HarnessState(TypedDict):
    """
    Complete state for HACI harness investigations.
    
    This TypedDict is used by LangGraph (running LOCALLY) to:
    - Track state across all nodes in the graph
    - Enable checkpointing for long-running investigations  
    - Support human-in-the-loop approval workflows
    - Persist state across restarts
    """
    
    # ─────────────────────────────────────────────────────────────────────────
    # Input Context
    # ─────────────────────────────────────────────────────────────────────────
    ticket_id: str
    ticket_description: str
    ticket_severity: Literal["low", "medium", "high", "critical"]
    customer_context: Optional[dict]
    
    # ─────────────────────────────────────────────────────────────────────────
    # Execution Configuration
    # ─────────────────────────────────────────────────────────────────────────
    execution_mode: Literal["single_agent", "micro_swarm", "full_swarm", "human_led"]
    agent_id: str
    max_iterations: int
    confidence_threshold: float
    
    # ─────────────────────────────────────────────────────────────────────────
    # THINK Phase Outputs (Annotated for list accumulation)
    # ─────────────────────────────────────────────────────────────────────────
    hypotheses: Annotated[List[Hypothesis], operator.add]
    investigation_plan: List[InvestigationStep]
    
    # ─────────────────────────────────────────────────────────────────────────
    # ACT Phase Outputs
    # ─────────────────────────────────────────────────────────────────────────
    tool_calls: Annotated[List[ToolCall], operator.add]
    pending_actions: List[InvestigationStep]
    
    # ─────────────────────────────────────────────────────────────────────────
    # OBSERVE Phase Outputs
    # ─────────────────────────────────────────────────────────────────────────
    observations: Annotated[List[Observation], operator.add]
    correlations: List[str]
    gaps: List[str]
    
    # ─────────────────────────────────────────────────────────────────────────
    # EVALUATE Phase Outputs
    # ─────────────────────────────────────────────────────────────────────────
    current_confidence: float
    decision: Literal["continue", "complete", "escalate", "await_human"]
    finding: Optional[str]
    escalation_reason: Optional[str]
    
    # ─────────────────────────────────────────────────────────────────────────
    # Loop Control
    # ─────────────────────────────────────────────────────────────────────────
    iteration_count: int
    current_phase: Literal["think", "act", "observe", "evaluate", "complete"]
    
    # ─────────────────────────────────────────────────────────────────────────
    # Human-in-the-Loop
    # ─────────────────────────────────────────────────────────────────────────
    requires_human_approval: bool
    human_feedback: Optional[str]
    approval_status: Optional[Literal["pending", "approved", "rejected"]]
```

> **Annotated Reducers:** The `Annotated[List[...], operator.add]` syntax tells LangGraph how to merge state updates. When a node returns `{"hypotheses": [new_hyp]}`, LangGraph appends to the existing list instead of replacing it. This is essential for accumulating findings across iterations.

### Build Harness Graph

The harness graph implements THINK→ACT→OBSERVE→EVALUATE as nodes with conditional routing back to THINK or forward to completion.

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  THINK   │───▶│   ACT    │───▶│ OBSERVE  │───▶│ EVALUATE │───▶│  ROUTER  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

```python
"""
HACI Harness Graph Implementation

File: src/graphs/harness_graph.py
Location: YOUR LOCAL MACHINE

This module creates the LangGraph StateGraph that implements the
THINK→ACT→OBSERVE→EVALUATE harness loop with conditional routing.

EXECUTION FLOW:
1. You run this code on YOUR LOCAL machine
2. LangGraph executes each node locally
3. The @traceable decorator sends trace data to LANGSMITH CLOUD
4. You view the execution trace at smith.langchain.com
"""

from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langsmith import traceable

from src.state.harness_state import HarnessState
from src.agents.base_agent import BaseAgent


# ============================================================================
# Phase Node Functions
# Each function runs LOCALLY, but @traceable sends traces to LangSmith CLOUD
# ============================================================================

@traceable(name="harness_think_phase")  # ← This sends trace data to LangSmith cloud
async def think_node(state: HarnessState, agent: BaseAgent) -> dict:
    """
    THINK Phase: Analyze input and form hypotheses.
    
    Execution: LOCAL
    Tracing: Sent to LANGSMITH CLOUD
    
    - Examines ticket description and context
    - Forms hypotheses about root cause
    - Creates investigation plan
    
    Returns partial state update with hypotheses and plan.
    """
    print(f"🧠 THINK Phase - Iteration {state['iteration_count'] + 1}")
    
    # Build context for thinking
    context = {
        "ticket": state["ticket_description"],
        "severity": state["ticket_severity"],
        "existing_hypotheses": [h.dict() for h in state["hypotheses"]],
        "observations": [o.dict() for o in state["observations"]],
        "gaps": state["gaps"],
    }
    
    # Call agent's think method (may call LLM API in cloud)
    result = await agent.think(context)
    
    return {
        "hypotheses": result["hypotheses"],
        "investigation_plan": result["investigation_plan"],
        "current_phase": "act",
    }


@traceable(name="harness_act_phase")
async def act_node(state: HarnessState, agent: BaseAgent) -> dict:
    """
    ACT Phase: Execute tools from investigation plan.
    
    Execution: LOCAL
    Tool APIs: May call external services (Datadog, GitHub, etc.)
    Tracing: Sent to LANGSMITH CLOUD
    """
    print(f"⚡ ACT Phase - Executing {len(state['investigation_plan'])} actions")
    
    tool_results = await agent.act(state["investigation_plan"])
    
    return {
        "tool_calls": tool_results,
        "pending_actions": [],
        "current_phase": "observe",
    }


@traceable(name="harness_observe_phase")
async def observe_node(state: HarnessState, agent: BaseAgent) -> dict:
    """
    OBSERVE Phase: Analyze tool results and extract insights.
    
    Execution: LOCAL
    Tracing: Sent to LANGSMITH CLOUD
    """
    print(f"👁️ OBSERVE Phase - Processing {len(state['tool_calls'])} results")
    
    recent_calls = state["tool_calls"][-len(state["investigation_plan"]):]
    
    observations = await agent.observe(
        tool_results=[tc.dict() for tc in recent_calls],
        hypotheses=[h.dict() for h in state["hypotheses"]]
    )
    
    return {
        "observations": observations["observations"],
        "correlations": observations.get("correlations", []),
        "gaps": observations.get("gaps", []),
        "current_phase": "evaluate",
    }


@traceable(name="harness_evaluate_phase")
async def evaluate_node(state: HarnessState, agent: BaseAgent) -> dict:
    """
    EVALUATE Phase: Determine next action based on findings.
    
    Execution: LOCAL
    Tracing: Sent to LANGSMITH CLOUD
    """
    print(f"✅ EVALUATE Phase - Confidence: {state['current_confidence']:.1%}")
    
    evaluation = await agent.evaluate(
        hypotheses=[h.dict() for h in state["hypotheses"]],
        observations=[o.dict() for o in state["observations"]],
        iteration=state["iteration_count"],
        max_iterations=state["max_iterations"],
        threshold=state["confidence_threshold"]
    )
    
    return {
        "current_confidence": evaluation["confidence"],
        "decision": evaluation["decision"],
        "finding": evaluation.get("finding"),
        "escalation_reason": evaluation.get("escalation_reason"),
        "iteration_count": state["iteration_count"] + 1,
        "requires_human_approval": evaluation.get("requires_human_approval", False),
    }


# ============================================================================
# Conditional Router (runs locally)
# ============================================================================

def route_after_evaluate(state: HarnessState) -> Literal["think", "complete", "escalate", "human_gate"]:
    """Route to next node based on EVALUATE decision."""
    decision = state["decision"]
    
    if decision == "continue":
        return "think"
    elif decision == "complete":
        return "complete"
    elif decision == "escalate":
        return "escalate"
    elif decision == "await_human":
        return "human_gate"
    else:
        return "think"


# ============================================================================
# Graph Assembly (runs locally)
# ============================================================================

def create_harness_graph(agent: BaseAgent, checkpointer=None):
    """
    Create the complete HACI harness graph.
    
    This function runs LOCALLY and creates a graph that:
    - Executes on your local machine or server
    - Sends traces to LangSmith cloud automatically
    - Can be viewed at smith.langchain.com
    """
    graph = StateGraph(HarnessState)
    
    # Add phase nodes
    graph.add_node("think", lambda s: think_node(s, agent))
    graph.add_node("act", lambda s: act_node(s, agent))
    graph.add_node("observe", lambda s: observe_node(s, agent))
    graph.add_node("evaluate", lambda s: evaluate_node(s, agent))
    
    # Add terminal nodes
    graph.add_node("complete", lambda s: {"current_phase": "complete"})
    graph.add_node("escalate", lambda s: {"current_phase": "escalate"})
    graph.add_node("human_gate", lambda s: {"approval_status": "pending"})
    
    # Add edges
    graph.add_edge(START, "think")
    graph.add_edge("think", "act")
    graph.add_edge("act", "observe")
    graph.add_edge("observe", "evaluate")
    
    graph.add_conditional_edges(
        "evaluate",
        route_after_evaluate,
        {
            "think": "think",
            "complete": "complete",
            "escalate": "escalate",
            "human_gate": "human_gate",
        }
    )
    
    graph.add_edge("complete", END)
    graph.add_edge("escalate", END)
    graph.add_edge("human_gate", "think")
    
    if checkpointer is None:
        checkpointer = MemorySaver()
    
    return graph.compile(checkpointer=checkpointer)
```

### Running the Graph

```python
"""
Example: Running the HACI harness graph

File: run_investigation.py
Location: YOUR LOCAL MACHINE

This script demonstrates the execution flow:
1. Initialize an agent (LOCAL)
2. Create a LangGraph (LOCAL)
3. Run the investigation (LOCAL)
4. Traces automatically sent to LangSmith (CLOUD)
5. View results at smith.langchain.com (CLOUD)
"""

import asyncio
import os
from dotenv import load_dotenv

# Load local .env file
load_dotenv()

from src.graphs.harness_graph import create_harness_graph
from src.agents.log_agent import LogAgent
from src.state.harness_state import create_initial_state


async def run_investigation():
    print("=" * 60)
    print("HACI Investigation Runner")
    print("=" * 60)
    print("\n📍 Execution: LOCAL")
    print("📊 Tracing: LANGSMITH CLOUD")
    print()
    
    # Initialize agent (runs locally)
    agent = LogAgent()
    
    # Create graph (runs locally)
    graph = create_harness_graph(agent)
    
    # Create initial state
    initial_state = create_initial_state(
        ticket_id="TICKET-1234",
        ticket_description="Application throwing 500 errors after deployment",
        ticket_severity="high",
        agent_id="log_agent",
        execution_mode="single_agent"
    )
    
    config = {
        "configurable": {
            "thread_id": "investigation-1234"
        }
    }
    
    # Execute (runs locally, traces sent to cloud)
    print("🚀 Starting investigation...")
    print("   (Traces being sent to LangSmith cloud)\n")
    
    result = await graph.ainvoke(initial_state, config)
    
    print(f"\n✅ Investigation complete!")
    print(f"   Decision: {result['decision']}")
    print(f"   Confidence: {result['current_confidence']:.1%}")
    print(f"   Finding: {result['finding']}")
    
    project = os.getenv('LANGCHAIN_PROJECT', 'default')
    print(f"\n🔍 View full trace at:")
    print(f"   https://smith.langchain.com/projects/{project}")


if __name__ == "__main__":
    asyncio.run(run_investigation())
```

---

## Chapter 4: Observability

### Understanding LangSmith Tracing

> **Key Concept:** Your code runs **locally**, but the `@traceable` decorator and `LANGCHAIN_TRACING_V2=true` environment variable cause trace data to be sent to **LangSmith cloud** automatically.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     YOUR LOCAL MACHINE                                   │
│                                                                         │
│   Your Code                                                             │
│      │                                                                  │
│      ▼                                                                  │
│   @traceable decorator ────────────────────┐                            │
│      │                                     │                            │
│      ▼                                     │ Trace data                 │
│   Function executes                        │ (sent automatically)       │
│      │                                     │                            │
│      ▼                                     ▼                            │
│   Result returned              ┌─────────────────────┐                  │
│                                │   HTTPS POST to     │                  │
│                                │   LangSmith API     │                  │
│                                └──────────┬──────────┘                  │
└───────────────────────────────────────────┼─────────────────────────────┘
                                            │
                                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     LANGSMITH CLOUD                                      │
│                     (smith.langchain.com)                               │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                     Trace Storage                               │   │
│   │   • Run history                                                 │   │
│   │   • Input/output logging                                        │   │
│   │   • Latency measurements                                        │   │
│   │   • Token usage tracking                                        │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                     Web Dashboard                               │   │
│   │   • Visual trace explorer                                       │   │
│   │   • Cost analytics                                              │   │
│   │   • Evaluation results                                          │   │
│   │   • Alerting & monitoring                                       │   │
│   └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### Viewing Traces in LangSmith

After running your code locally, view traces in the LangSmith web UI:

1. **Go to** [smith.langchain.com](https://smith.langchain.com) in your browser
2. **Select your project** (e.g., `haci-production`)
3. **Click on a trace** to see the full execution flow
4. **Expand nodes** to see inputs, outputs, and timing

**What you'll see in LangSmith:**
```
LangSmith Dashboard (Web UI at smith.langchain.com)
├── Projects
│   └── haci-production
│       ├── Runs (list of all executions from your local code)
│       │   └── investigation-1234
│       │       ├── harness_think_phase (2.3s)
│       │       │   ├── Input: ticket context
│       │       │   ├── Output: hypotheses
│       │       │   └── LLM call to Anthropic
│       │       ├── harness_act_phase (1.8s)
│       │       ├── harness_observe_phase (1.2s)
│       │       └── harness_evaluate_phase (0.8s)
│       ├── Datasets (test data you create)
│       ├── Evaluators (accuracy metrics)
│       └── Monitoring (alerts & dashboards)
```

---

## Quick Reference: Local vs. Cloud

| Task | Where | How |
|------|-------|-----|
| Write Python code | **Local** | Your IDE/editor |
| Create project directories | **Local** | `mkdir` command |
| Install dependencies | **Local** | `pip install` |
| Run HACI investigations | **Local** | `python run_investigation.py` |
| View execution traces | **LangSmith Cloud** | smith.langchain.com |
| Create evaluation datasets | **LangSmith Cloud** | Web UI or API |
| Set up monitoring alerts | **LangSmith Cloud** | Web UI |
| Store API keys | **Local** (.env file) | Never commit to Git |
| Make LLM calls | **LLM Provider Cloud** | Via API (Anthropic, OpenAI) |
| Deploy to production | **Your servers/cloud** | Docker, Kubernetes, etc. |

---

## Summary

This guide covered the implementation of HACI on LangSmith:

1. **Setup** - Local environment configuration with cloud connections
2. **Graph Architecture** - State schema and LangGraph design (runs locally)
3. **Agent Implementation** - Specialist agents with tool binding (runs locally)
4. **Observability** - Tracing to LangSmith cloud for monitoring

**The key distinction to remember:**
- **LOCAL:** Your code, LangGraph execution, tool integrations, state management
- **LANGSMITH CLOUD:** Trace viewing, evaluation datasets, monitoring dashboards
- **LLM CLOUD:** AI reasoning (Anthropic/OpenAI API calls)

For complete documentation on remaining chapters (5-10), see the extended implementation guide covering:
- Chapter 5: Harness Phases Deep Dive
- Chapter 6: Multi-Agent Swarm Coordination  
- Chapter 7: Context Engineering Integration
- Chapter 8: Human-in-the-Loop Patterns
- Chapter 9: Testing & Evaluation
- Chapter 10: Production Deployment

For more information:
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Anthropic Documentation](https://docs.anthropic.com/)

---

*HACI Implementation Guide - Built for enterprise-grade AI automation with calibrated autonomy and human oversight.*
