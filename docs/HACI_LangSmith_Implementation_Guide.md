# HACI on LangSmith: Complete Implementation Guide

> Build a production-ready Harness-Enhanced Agentic Collaborative Intelligence system using LangGraph and LangSmith

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

**LangGraph Benefits:**
- **Stateful Workflows:** Built-in persistence for long-running agent operations
- **Graph-Based Control:** Define agent interactions as nodes and edges
- **Human-in-the-Loop:** Native interrupt/resume for approval gates
- **Checkpointing:** Automatic state snapshots for recovery
- **Multi-Agent Patterns:** Supervisor, network, and hierarchical architectures

**LangSmith Benefits:**
- **Deep Tracing:** Visualize every step of agent reasoning
- **Token Analytics:** Track costs per agent, per investigation
- **Evaluation Datasets:** Build test suites from production traces
- **Real-Time Monitoring:** Alerts for latency, errors, cost spikes
- **Prompt Management:** Version and A/B test system prompts

> **Perfect Fit for HACI:** HACI's THINK→ACT→OBSERVE→EVALUATE harness maps naturally to LangGraph nodes. Each phase becomes a node, the harness loop becomes a cycle in the graph, and multi-agent swarms become parallel branches that converge at a coordinator node.

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LANGSMITH OBSERVABILITY                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Tracing   │  │  Datasets   │  │ Evaluators  │  │  Monitoring │        │
│  │  (All Runs) │  │ (Test Data) │  │ (Accuracy)  │  │  (Alerts)   │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
└─────────┼────────────────┼────────────────┼────────────────┼────────────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LANGGRAPH EXECUTION ENGINE                          │
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

| Requirement | Details | Status |
|-------------|---------|--------|
| **LangSmith Account** | Sign up at smith.langchain.com. Free tier available for development. | Required |
| **Python 3.11+** | LangGraph requires Python 3.11 or higher for full async support. | Required |
| **LLM API Keys** | Anthropic (Claude), OpenAI (GPT-4), or other supported providers. | Required |
| **Redis** | For context bus implementation (can use Docker locally). | Optional |
| **PostgreSQL** | For LangGraph checkpointing and HACI's System of Record. | Optional |
| **Docker** | For local development infrastructure and LangGraph Studio. | Optional |

### Installation

#### Step 1: Create Project Directory

```bash
# Create project structure
mkdir haci-langsmith && cd haci-langsmith

# Create directory structure
mkdir -p src/{agents,graphs,tools,memory,utils}
mkdir -p tests/{unit,integration,e2e}
mkdir -p config

# Initialize Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Step 2: Install Dependencies

**requirements.txt:**
```txt
# Core LangChain ecosystem
langgraph>=0.2.0
langchain>=0.3.0
langchain-anthropic>=0.2.0
langchain-openai>=0.2.0
langsmith>=0.1.0

# LLM providers
anthropic>=0.34.0
openai>=1.50.0

# State management
redis>=5.0.0
asyncpg>=0.29.0
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

Install with:
```bash
pip install -r requirements.txt
```

#### Step 3: Configure Environment Variables

**.env:**
```bash
# LangSmith Configuration
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_pt_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LANGCHAIN_PROJECT=haci-production
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com

# LLM Providers
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Infrastructure (Optional)
REDIS_URL=redis://localhost:6379/0
DATABASE_URL=postgresql://user:pass@localhost:5432/haci

# HACI Configuration
HACI_MAX_ITERATIONS=10
HACI_DEFAULT_CONFIDENCE_THRESHOLD=0.80
HACI_ENABLE_HUMAN_APPROVAL=true
```

#### Step 4: Verify Installation

```python
# verify_setup.py
import os
from langsmith import Client
from langgraph.graph import StateGraph

def verify_setup():
    # Check LangSmith connection
    client = Client()
    print(f"✅ LangSmith connected: {client.api_url}")
    
    # Verify project exists
    project = os.getenv("LANGCHAIN_PROJECT", "default")
    print(f"✅ Project: {project}")
    
    # Test LangGraph import
    graph = StateGraph(dict)
    print("✅ LangGraph available")
    
    print("\n🎉 Setup complete! Ready to build HACI.")

if __name__ == "__main__":
    verify_setup()
```

### Project Structure

```
haci-langsmith/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py      # Abstract agent interface
│   │   ├── log_agent.py       # Log analysis specialist
│   │   ├── code_agent.py      # Code analysis specialist
│   │   ├── infra_agent.py     # Infrastructure specialist
│   │   ├── db_agent.py        # Database specialist
│   │   └── security_agent.py  # Security specialist
│   ├── graphs/
│   │   ├── __init__.py
│   │   ├── harness_graph.py   # THINK→ACT→OBSERVE→EVALUATE
│   │   └── swarm_graph.py     # Multi-agent coordination
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── datadog_tools.py   # Monitoring tools
│   │   ├── github_tools.py    # Code repository tools
│   │   ├── jira_tools.py      # Issue tracking tools
│   │   └── aws_tools.py       # Cloud infrastructure tools
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── context_bus.py     # Redis-based context sharing
│   │   └── checkpointer.py    # PostgreSQL state persistence
│   └── utils/
│       ├── __init__.py
│       ├── prompts.py         # System prompts
│       └── config.py          # Configuration management
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── config/
│   └── settings.yaml
├── .env
├── requirements.txt
└── README.md
```

---

## Chapter 2: Graph Architecture

### State Schema Design

The HarnessState TypedDict defines all data that flows through the investigation graph. LangGraph uses this schema to track state across nodes and persist between runs.

```python
"""
HACI Harness State Schema

This TypedDict defines the complete state structure for HACI investigations.
LangGraph uses this to track state across nodes and enable checkpointing.
"""

from typing import TypedDict, Annotated, Optional, List, Literal
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
    
    This TypedDict is used by LangGraph to:
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

This module creates the LangGraph StateGraph that implements the
THINK→ACT→OBSERVE→EVALUATE harness loop with conditional routing.
"""

from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langsmith import traceable

from src.state.harness_state import HarnessState
from src.agents.base_agent import BaseAgent


# ============================================================================
# Phase Node Functions
# ============================================================================

@traceable(name="harness_think_phase")
async def think_node(state: HarnessState, agent: BaseAgent) -> dict:
    """
    THINK Phase: Analyze input and form hypotheses.
    
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
    
    # Call agent's think method
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
    
    - Executes tools specified in the plan
    - Respects mode-specific constraints (max tools, timeouts)
    - Handles tool errors gracefully
    
    Returns partial state update with tool call results.
    """
    print(f"⚡ ACT Phase - Executing {len(state['investigation_plan'])} actions")
    
    # Execute investigation plan
    tool_results = await agent.act(state["investigation_plan"])
    
    return {
        "tool_calls": tool_results,
        "pending_actions": [],  # Clear pending
        "current_phase": "observe",
    }


@traceable(name="harness_observe_phase")
async def observe_node(state: HarnessState, agent: BaseAgent) -> dict:
    """
    OBSERVE Phase: Analyze tool results and extract insights.
    
    - Processes tool outputs
    - Identifies patterns and correlations
    - Updates hypothesis confidence
    - Identifies remaining gaps
    
    Returns partial state update with observations.
    """
    print(f"👁️ OBSERVE Phase - Processing {len(state['tool_calls'])} results")
    
    # Get recent tool calls from this iteration
    recent_calls = state["tool_calls"][-len(state["investigation_plan"]):]
    
    # Analyze results
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
    
    - Calculates overall confidence
    - Decides: continue, complete, escalate, or await human
    - Checks iteration limits and other constraints
    
    Returns partial state update with decision.
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
# Conditional Router
# ============================================================================

def route_after_evaluate(state: HarnessState) -> Literal["think", "complete", "escalate", "human_gate"]:
    """
    Route to next node based on EVALUATE decision.
    
    Returns:
        - "think": Continue investigation loop
        - "complete": Investigation finished successfully
        - "escalate": Human intervention required
        - "human_gate": Await human approval before proceeding
    """
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
        # Default to continue if unknown
        return "think"


# ============================================================================
# Graph Assembly
# ============================================================================

def create_harness_graph(agent: BaseAgent, checkpointer=None):
    """
    Create the complete HACI harness graph.
    
    Args:
        agent: The agent instance to use for all phases
        checkpointer: Optional checkpointer for state persistence
        
    Returns:
        Compiled LangGraph ready for execution
    """
    # Create graph with state schema
    graph = StateGraph(HarnessState)
    
    # Add phase nodes (using closures to bind agent)
    graph.add_node("think", lambda s: think_node(s, agent))
    graph.add_node("act", lambda s: act_node(s, agent))
    graph.add_node("observe", lambda s: observe_node(s, agent))
    graph.add_node("evaluate", lambda s: evaluate_node(s, agent))
    
    # Add terminal nodes
    graph.add_node("complete", lambda s: {"current_phase": "complete"})
    graph.add_node("escalate", lambda s: {"current_phase": "escalate"})
    graph.add_node("human_gate", lambda s: {"approval_status": "pending"})
    
    # Add sequential edges for main flow
    graph.add_edge(START, "think")
    graph.add_edge("think", "act")
    graph.add_edge("act", "observe")
    graph.add_edge("observe", "evaluate")
    
    # Add conditional routing after evaluate
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
    
    # Terminal nodes go to END
    graph.add_edge("complete", END)
    graph.add_edge("escalate", END)
    
    # Human gate can resume to think after approval
    graph.add_edge("human_gate", "think")
    
    # Compile with optional checkpointer
    if checkpointer is None:
        checkpointer = MemorySaver()
    
    return graph.compile(checkpointer=checkpointer)
```

### Running the Graph

```python
"""Example: Running the HACI harness graph"""

import asyncio
from src.graphs.harness_graph import create_harness_graph
from src.agents.log_agent import LogAgent
from src.state.harness_state import create_initial_state

async def run_investigation():
    # Initialize agent
    agent = LogAgent()
    
    # Create graph with in-memory checkpointing
    graph = create_harness_graph(agent)
    
    # Create initial state
    initial_state = create_initial_state(
        ticket_id="TICKET-1234",
        ticket_description="Application throwing 500 errors after deployment",
        ticket_severity="high",
        agent_id="log_agent",
        execution_mode="single_agent"
    )
    
    # Configure run with thread_id for checkpointing
    config = {
        "configurable": {
            "thread_id": "investigation-1234"
        }
    }
    
    # Execute graph
    result = await graph.ainvoke(initial_state, config)
    
    print(f"Investigation complete!")
    print(f"Decision: {result['decision']}")
    print(f"Confidence: {result['current_confidence']:.1%}")
    print(f"Finding: {result['finding']}")

if __name__ == "__main__":
    asyncio.run(run_investigation())
```

---

## Chapter 3: Agent Implementation

### Base Agent Interface

```python
"""
Base Agent Abstract Class

All HACI agents implement this interface to ensure consistent
behavior across the harness phases.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import BaseTool
from langsmith import traceable


class BaseAgent(ABC):
    """
    Abstract base class for HACI specialist agents.
    
    Each agent must implement:
    - think(): Form hypotheses and create investigation plan
    - act(): Execute tools based on the plan
    - observe(): Analyze results and extract insights
    - evaluate(): Determine next action
    """
    
    def __init__(
        self,
        agent_id: str,
        llm: ChatAnthropic = None,
        tools: List[BaseTool] = None,
        system_prompt: str = None
    ):
        self.agent_id = agent_id
        self.llm = llm or ChatAnthropic(model="claude-sonnet-4-20250514")
        self.tools = tools or []
        self.system_prompt = system_prompt or self._default_system_prompt()
        
        # Bind tools to LLM if available
        if self.tools:
            self.llm_with_tools = self.llm.bind_tools(self.tools)
        else:
            self.llm_with_tools = self.llm
    
    @abstractmethod
    def _default_system_prompt(self) -> str:
        """Return the default system prompt for this agent type."""
        pass
    
    @abstractmethod
    @traceable(name="agent_think")
    async def think(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        THINK Phase: Analyze context and form hypotheses.
        
        Args:
            context: Current investigation context including ticket,
                    existing hypotheses, observations, and gaps.
        
        Returns:
            Dict with 'hypotheses' and 'investigation_plan' keys.
        """
        pass
    
    @abstractmethod
    @traceable(name="agent_act")
    async def act(self, plan: List[Dict]) -> List[Dict]:
        """
        ACT Phase: Execute investigation plan.
        
        Args:
            plan: List of InvestigationStep dicts specifying
                 tools to call and their arguments.
        
        Returns:
            List of ToolCall dicts with results.
        """
        pass
    
    @abstractmethod
    @traceable(name="agent_observe")
    async def observe(
        self,
        tool_results: List[Dict],
        hypotheses: List[Dict]
    ) -> Dict[str, Any]:
        """
        OBSERVE Phase: Analyze tool results.
        
        Args:
            tool_results: Results from ACT phase tool calls.
            hypotheses: Current hypotheses to evaluate.
        
        Returns:
            Dict with 'observations', 'correlations', 'gaps' keys.
        """
        pass
    
    @abstractmethod
    @traceable(name="agent_evaluate")
    async def evaluate(
        self,
        hypotheses: List[Dict],
        observations: List[Dict],
        iteration: int,
        max_iterations: int,
        threshold: float
    ) -> Dict[str, Any]:
        """
        EVALUATE Phase: Determine next action.
        
        Args:
            hypotheses: All hypotheses with confidence levels.
            observations: All observations from investigation.
            iteration: Current iteration number.
            max_iterations: Maximum allowed iterations.
            threshold: Confidence threshold for completion.
        
        Returns:
            Dict with 'confidence', 'decision', optional 'finding'.
        """
        pass
```

### Log Analysis Agent

```python
"""
Log Analysis Specialist Agent

Expert in analyzing application logs, error patterns, and system events.
"""

from typing import List, Dict, Any
from langsmith import traceable
from src.agents.base_agent import BaseAgent
from src.tools.datadog_tools import (
    search_logs,
    get_log_patterns,
    get_error_frequency
)


class LogAgent(BaseAgent):
    """
    Specialist agent for log analysis investigations.
    
    Capabilities:
    - Search and filter log entries
    - Identify error patterns and anomalies
    - Correlate log events with deployments
    - Trace request flows across services
    """
    
    def __init__(self):
        super().__init__(
            agent_id="log_agent",
            tools=[search_logs, get_log_patterns, get_error_frequency]
        )
    
    def _default_system_prompt(self) -> str:
        return """You are a Log Analysis Specialist for HACI.

Your expertise includes:
- Analyzing application and system logs
- Identifying error patterns and anomalies
- Correlating events across distributed systems
- Recognizing deployment-related issues

When investigating:
1. Start with error logs from the affected timeframe
2. Look for patterns in error frequency and types
3. Trace related events across services
4. Correlate with recent deployments or changes

Always cite specific log entries as evidence for your hypotheses.
Format timestamps consistently and note log sources."""
    
    @traceable(name="log_agent_think")
    async def think(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Form hypotheses based on ticket and existing findings."""
        
        prompt = f"""Analyze this support ticket and form hypotheses:

Ticket: {context['ticket']}
Severity: {context['severity']}

Existing Hypotheses: {context.get('existing_hypotheses', [])}
Previous Observations: {context.get('observations', [])}
Identified Gaps: {context.get('gaps', [])}

Based on this information:
1. Form 1-3 hypotheses about the root cause
2. Create an investigation plan with specific log queries

Respond in JSON format:
{{
    "hypotheses": [
        {{
            "id": "hyp_1",
            "description": "...",
            "confidence": 0.0,
            "evidence_for": [],
            "evidence_against": []
        }}
    ],
    "investigation_plan": [
        {{
            "tool": "search_logs",
            "purpose": "Find error logs...",
            "arguments": {{"query": "...", "timeframe": "1h"}},
            "priority": 1
        }}
    ]
}}"""

        response = await self.llm.ainvoke(prompt)
        return self._parse_think_response(response.content)
    
    @traceable(name="log_agent_act")
    async def act(self, plan: List[Dict]) -> List[Dict]:
        """Execute log analysis tools."""
        results = []
        
        for step in sorted(plan, key=lambda x: x.get("priority", 1)):
            tool_name = step["tool"]
            args = step["arguments"]
            
            try:
                # Find and execute the tool
                tool = next(t for t in self.tools if t.name == tool_name)
                result = await tool.ainvoke(args)
                
                results.append({
                    "tool_name": tool_name,
                    "arguments": args,
                    "result": result,
                    "error": None
                })
            except Exception as e:
                results.append({
                    "tool_name": tool_name,
                    "arguments": args,
                    "result": None,
                    "error": str(e)
                })
        
        return results
    
    @traceable(name="log_agent_observe")
    async def observe(
        self,
        tool_results: List[Dict],
        hypotheses: List[Dict]
    ) -> Dict[str, Any]:
        """Analyze log query results."""
        
        prompt = f"""Analyze these log query results:

Tool Results:
{tool_results}

Current Hypotheses:
{hypotheses}

Extract:
1. Key observations from the logs
2. Correlations between different log sources
3. Remaining gaps in our understanding

Respond in JSON:
{{
    "observations": [
        {{
            "id": "obs_1",
            "source_tool": "search_logs",
            "finding": "...",
            "relevance": 0.8,
            "supports_hypothesis": "hyp_1"
        }}
    ],
    "correlations": ["..."],
    "gaps": ["..."]
}}"""

        response = await self.llm.ainvoke(prompt)
        return self._parse_observe_response(response.content)
    
    @traceable(name="log_agent_evaluate")
    async def evaluate(
        self,
        hypotheses: List[Dict],
        observations: List[Dict],
        iteration: int,
        max_iterations: int,
        threshold: float
    ) -> Dict[str, Any]:
        """Evaluate investigation progress and decide next action."""
        
        # Calculate confidence based on evidence
        best_hypothesis = max(hypotheses, key=lambda h: h.get("confidence", 0))
        confidence = best_hypothesis.get("confidence", 0)
        
        # Decision logic
        if confidence >= threshold:
            return {
                "confidence": confidence,
                "decision": "complete",
                "finding": best_hypothesis["description"],
                "requires_human_approval": confidence < 0.95
            }
        elif iteration >= max_iterations:
            return {
                "confidence": confidence,
                "decision": "escalate",
                "escalation_reason": f"Max iterations ({max_iterations}) reached"
            }
        else:
            return {
                "confidence": confidence,
                "decision": "continue"
            }
```

---

## Chapter 4: Observability

### LangSmith Tracing Integration

Every node, tool call, and LLM invocation is automatically traced with the `@traceable` decorator.

```python
"""
Comprehensive Tracing with LangSmith

This module shows how to add rich observability to HACI components.
"""

from langsmith import traceable
from langsmith.run_helpers import get_current_run_tree
import structlog

logger = structlog.get_logger()


@traceable(
    name="harness_investigation",
    metadata={
        "component": "harness",
        "version": "1.0.0"
    }
)
async def run_investigation(state: HarnessState) -> HarnessState:
    """
    Top-level traceable wrapper for investigations.
    
    This creates a parent trace that contains all child operations.
    """
    # Get current run for correlation
    run_tree = get_current_run_tree()
    trace_id = run_tree.id if run_tree else "unknown"
    
    logger.info(
        "investigation_started",
        ticket_id=state["ticket_id"],
        trace_id=trace_id,
        mode=state["execution_mode"]
    )
    
    # Run the graph
    result = await graph.ainvoke(state)
    
    logger.info(
        "investigation_complete",
        ticket_id=state["ticket_id"],
        trace_id=trace_id,
        decision=result["decision"],
        confidence=result["current_confidence"]
    )
    
    return result


@traceable(name="tool_execution", run_type="tool")
async def execute_tool_with_tracing(
    tool_name: str,
    arguments: dict,
    timeout: float = 30.0
) -> dict:
    """
    Execute a tool with full tracing and error handling.
    
    The run_type="tool" ensures proper categorization in LangSmith.
    """
    import time
    start = time.time()
    
    try:
        result = await tool.ainvoke(arguments)
        duration_ms = int((time.time() - start) * 1000)
        
        return {
            "tool_name": tool_name,
            "result": result,
            "duration_ms": duration_ms,
            "error": None
        }
    except Exception as e:
        duration_ms = int((time.time() - start) * 1000)
        
        return {
            "tool_name": tool_name,
            "result": None,
            "duration_ms": duration_ms,
            "error": str(e)
        }
```

### Custom Metadata for Filtering

```python
"""Adding custom metadata to traces for advanced filtering."""

from langsmith import traceable
from functools import wraps


def traceable_with_context(name: str):
    """
    Custom decorator that adds HACI-specific context to traces.
    """
    def decorator(func):
        @wraps(func)
        @traceable(name=name)
        async def wrapper(state: HarnessState, *args, **kwargs):
            # Add rich metadata from state
            from langsmith.run_helpers import get_current_run_tree
            
            run_tree = get_current_run_tree()
            if run_tree:
                run_tree.metadata.update({
                    "ticket_id": state["ticket_id"],
                    "severity": state["ticket_severity"],
                    "execution_mode": state["execution_mode"],
                    "iteration": state["iteration_count"],
                    "agent_id": state.get("agent_id", "unknown"),
                })
            
            return await func(state, *args, **kwargs)
        return wrapper
    return decorator


# Usage
@traceable_with_context("think_phase")
async def think_node(state: HarnessState, agent: BaseAgent) -> dict:
    """Now automatically includes ticket_id, severity, etc. in trace."""
    ...
```

### Token Usage Tracking

```python
"""Track token usage and costs across agents."""

from langsmith import Client
from datetime import datetime, timedelta

client = Client()


def get_token_usage_by_agent(
    project: str = "haci-production",
    days: int = 7
) -> dict:
    """
    Aggregate token usage by agent_id.
    
    Returns dict mapping agent_id to token counts.
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)
    
    runs = client.list_runs(
        project_name=project,
        start_time=start_time,
        end_time=end_time,
        run_type="llm"
    )
    
    usage_by_agent = {}
    for run in runs:
        agent_id = run.metadata.get("agent_id", "unknown")
        tokens = run.total_tokens or 0
        
        if agent_id not in usage_by_agent:
            usage_by_agent[agent_id] = {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "run_count": 0
            }
        
        usage_by_agent[agent_id]["prompt_tokens"] += run.prompt_tokens or 0
        usage_by_agent[agent_id]["completion_tokens"] += run.completion_tokens or 0
        usage_by_agent[agent_id]["total_tokens"] += tokens
        usage_by_agent[agent_id]["run_count"] += 1
    
    return usage_by_agent
```

---

## Chapter 5: Harness Phases Deep Dive

### THINK Phase Implementation

The THINK phase generates hypotheses and creates an investigation plan. This is where the agent reasons about what might be wrong.

```python
"""
THINK Phase - Detailed Implementation

The THINK phase is the reasoning engine of HACI. It:
1. Analyzes the input ticket and context
2. Forms hypotheses about potential root causes
3. Creates a prioritized investigation plan
4. Adapts based on previous iteration findings
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field
from langsmith import traceable
from langchain_core.prompts import ChatPromptTemplate


class ThinkOutput(BaseModel):
    """Structured output from THINK phase."""
    hypotheses: List[Hypothesis] = Field(
        description="Ranked hypotheses about root cause"
    )
    investigation_plan: List[InvestigationStep] = Field(
        description="Prioritized list of actions to take"
    )
    reasoning: str = Field(
        description="Explanation of thinking process"
    )


THINK_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are the THINK phase of the HACI investigation system.

Your role is to:
1. Analyze the support ticket and all available context
2. Form 1-3 hypotheses about the root cause
3. Create a focused investigation plan

Guidelines:
- Prioritize hypotheses by likelihood
- Each hypothesis should be testable with available tools
- Investigation steps should directly test hypotheses
- Build on previous findings if this isn't the first iteration
- Identify what evidence would confirm or reject each hypothesis

Available tools: {available_tools}
Current iteration: {iteration} of {max_iterations}"""),
    
    ("human", """Analyze this situation:

Ticket: {ticket_description}
Severity: {severity}
Customer Context: {customer_context}

Previous Hypotheses: {existing_hypotheses}
Previous Observations: {observations}
Identified Gaps: {gaps}

Form hypotheses and create an investigation plan.""")
])


@traceable(name="think_phase_detailed")
async def think_phase(
    state: HarnessState,
    agent: BaseAgent
) -> Dict[str, Any]:
    """
    Execute the THINK phase with structured output.
    """
    # Build the prompt
    prompt = THINK_PROMPT.format(
        available_tools=[t.name for t in agent.tools],
        iteration=state["iteration_count"] + 1,
        max_iterations=state["max_iterations"],
        ticket_description=state["ticket_description"],
        severity=state["ticket_severity"],
        customer_context=state.get("customer_context", {}),
        existing_hypotheses=[h.dict() for h in state["hypotheses"]],
        observations=[o.dict() for o in state["observations"]],
        gaps=state["gaps"]
    )
    
    # Get structured output
    llm_with_structure = agent.llm.with_structured_output(ThinkOutput)
    result = await llm_with_structure.ainvoke(prompt)
    
    return {
        "hypotheses": result.hypotheses,
        "investigation_plan": result.investigation_plan,
        "current_phase": "act"
    }
```

### ACT Phase Implementation

The ACT phase executes the investigation plan by calling tools.

```python
"""
ACT Phase - Tool Execution

The ACT phase:
1. Executes tools from the investigation plan
2. Handles errors gracefully
3. Respects rate limits and timeouts
4. Tracks execution metrics
"""

import asyncio
from typing import List, Dict
from langsmith import traceable


@traceable(name="act_phase_detailed")
async def act_phase(
    state: HarnessState,
    agent: BaseAgent,
    max_concurrent: int = 3
) -> Dict[str, Any]:
    """
    Execute investigation plan with concurrency control.
    """
    plan = state["investigation_plan"]
    results = []
    
    # Group by priority for ordered execution
    priority_groups = {}
    for step in plan:
        priority = step.get("priority", 1)
        if priority not in priority_groups:
            priority_groups[priority] = []
        priority_groups[priority].append(step)
    
    # Execute each priority group
    for priority in sorted(priority_groups.keys()):
        group = priority_groups[priority]
        
        # Execute group with concurrency limit
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def execute_with_limit(step):
            async with semaphore:
                return await execute_tool_step(step, agent)
        
        group_results = await asyncio.gather(
            *[execute_with_limit(step) for step in group],
            return_exceptions=True
        )
        
        # Process results
        for step, result in zip(group, group_results):
            if isinstance(result, Exception):
                results.append({
                    "tool_name": step["tool"],
                    "arguments": step["arguments"],
                    "result": None,
                    "error": str(result)
                })
            else:
                results.append(result)
    
    return {
        "tool_calls": results,
        "pending_actions": [],
        "current_phase": "observe"
    }


@traceable(name="tool_step_execution", run_type="tool")
async def execute_tool_step(
    step: Dict,
    agent: BaseAgent,
    timeout: float = 30.0
) -> Dict:
    """Execute a single tool step with timeout."""
    import time
    
    tool_name = step["tool"]
    arguments = step["arguments"]
    
    # Find the tool
    tool = next(
        (t for t in agent.tools if t.name == tool_name),
        None
    )
    
    if not tool:
        return {
            "tool_name": tool_name,
            "arguments": arguments,
            "result": None,
            "error": f"Tool '{tool_name}' not found"
        }
    
    start = time.time()
    
    try:
        # Execute with timeout
        result = await asyncio.wait_for(
            tool.ainvoke(arguments),
            timeout=timeout
        )
        
        return {
            "tool_name": tool_name,
            "arguments": arguments,
            "result": result,
            "error": None,
            "duration_ms": int((time.time() - start) * 1000)
        }
    except asyncio.TimeoutError:
        return {
            "tool_name": tool_name,
            "arguments": arguments,
            "result": None,
            "error": f"Timeout after {timeout}s",
            "duration_ms": int(timeout * 1000)
        }
    except Exception as e:
        return {
            "tool_name": tool_name,
            "arguments": arguments,
            "result": None,
            "error": str(e),
            "duration_ms": int((time.time() - start) * 1000)
        }
```

### OBSERVE Phase Implementation

The OBSERVE phase analyzes tool results and extracts insights.

```python
"""
OBSERVE Phase - Result Analysis

The OBSERVE phase:
1. Processes tool outputs
2. Extracts meaningful observations
3. Updates hypothesis confidence
4. Identifies correlations and gaps
"""

from langsmith import traceable
from langchain_core.prompts import ChatPromptTemplate


OBSERVE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are the OBSERVE phase of the HACI investigation system.

Your role is to:
1. Analyze tool results objectively
2. Extract key observations
3. Update hypothesis confidence based on evidence
4. Identify correlations between findings
5. Note remaining gaps in understanding

Be precise about what the data shows vs. what it implies.
Always cite specific evidence for conclusions."""),
    
    ("human", """Analyze these tool results:

{tool_results}

Current Hypotheses:
{hypotheses}

Extract observations and update hypothesis confidence.""")
])


class ObserveOutput(BaseModel):
    """Structured output from OBSERVE phase."""
    observations: List[Observation]
    updated_hypotheses: List[Hypothesis]
    correlations: List[str]
    gaps: List[str]


@traceable(name="observe_phase_detailed")
async def observe_phase(
    state: HarnessState,
    agent: BaseAgent
) -> Dict[str, Any]:
    """
    Analyze tool results and extract insights.
    """
    # Get recent tool calls
    recent_results = state["tool_calls"][-len(state["investigation_plan"]):]
    
    # Format for analysis
    formatted_results = []
    for tc in recent_results:
        formatted_results.append({
            "tool": tc["tool_name"],
            "result": tc["result"][:2000] if tc["result"] else None,  # Truncate long results
            "error": tc.get("error")
        })
    
    prompt = OBSERVE_PROMPT.format(
        tool_results=formatted_results,
        hypotheses=[h.dict() for h in state["hypotheses"]]
    )
    
    llm_with_structure = agent.llm.with_structured_output(ObserveOutput)
    result = await llm_with_structure.ainvoke(prompt)
    
    return {
        "observations": result.observations,
        "hypotheses": result.updated_hypotheses,
        "correlations": result.correlations,
        "gaps": result.gaps,
        "current_phase": "evaluate"
    }
```

### EVALUATE Phase Implementation

The EVALUATE phase determines the next action based on findings.

```python
"""
EVALUATE Phase - Decision Making

The EVALUATE phase:
1. Calculates overall confidence
2. Applies decision rules
3. Determines: continue, complete, escalate, or await human
4. Respects iteration limits and thresholds
"""

from typing import Literal
from langsmith import traceable


class EvaluateOutput(BaseModel):
    """Structured output from EVALUATE phase."""
    confidence: float = Field(ge=0.0, le=1.0)
    decision: Literal["continue", "complete", "escalate", "await_human"]
    finding: Optional[str] = None
    escalation_reason: Optional[str] = None
    requires_human_approval: bool = False
    reasoning: str


@traceable(name="evaluate_phase_detailed")
async def evaluate_phase(
    state: HarnessState,
    agent: BaseAgent
) -> Dict[str, Any]:
    """
    Evaluate progress and decide next action.
    """
    # Get best hypothesis
    hypotheses = state["hypotheses"]
    if not hypotheses:
        return {
            "current_confidence": 0.0,
            "decision": "continue",
            "iteration_count": state["iteration_count"] + 1
        }
    
    best_hyp = max(hypotheses, key=lambda h: h.confidence)
    confidence = best_hyp.confidence
    
    # Check iteration limit
    if state["iteration_count"] >= state["max_iterations"]:
        return {
            "current_confidence": confidence,
            "decision": "escalate",
            "escalation_reason": f"Max iterations ({state['max_iterations']}) reached",
            "iteration_count": state["iteration_count"] + 1
        }
    
    # Check confidence threshold
    threshold = state["confidence_threshold"]
    
    if confidence >= threshold:
        # High confidence - check if human approval needed
        requires_approval = should_require_human_approval(state, confidence)
        
        if requires_approval:
            return {
                "current_confidence": confidence,
                "decision": "await_human",
                "finding": best_hyp.description,
                "requires_human_approval": True,
                "iteration_count": state["iteration_count"] + 1
            }
        else:
            return {
                "current_confidence": confidence,
                "decision": "complete",
                "finding": best_hyp.description,
                "iteration_count": state["iteration_count"] + 1
            }
    
    # Continue investigating
    return {
        "current_confidence": confidence,
        "decision": "continue",
        "iteration_count": state["iteration_count"] + 1
    }


def should_require_human_approval(state: HarnessState, confidence: float) -> bool:
    """
    Determine if human approval is required.
    
    Based on:
    - Execution mode
    - Ticket severity
    - Confidence level
    - Customer tier
    """
    mode = state["execution_mode"]
    severity = state["ticket_severity"]
    
    # Human-led mode always requires approval
    if mode == "human_led":
        return True
    
    # Critical severity requires approval
    if severity == "critical":
        return True
    
    # High severity with confidence < 95% requires approval
    if severity == "high" and confidence < 0.95:
        return True
    
    # Enterprise customers require approval for any action
    customer = state.get("customer_context", {})
    if customer.get("tier") == "enterprise":
        return True
    
    return False
```

---

## Chapter 6: Multi-Agent Swarm Coordination

### Swarm Architecture

For complex issues, multiple specialist agents work in parallel and synthesize their findings.

```python
"""
Multi-Agent Swarm Graph

Implements parallel agent execution with coordinated synthesis.
Uses LangGraph's Send API for dynamic fan-out.
"""

from typing import List, Dict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langsmith import traceable


class SwarmState(TypedDict):
    """State for swarm coordination."""
    ticket_id: str
    ticket_description: str
    ticket_severity: str
    
    # Agent assignments
    assigned_agents: List[str]
    
    # Agent results (accumulated)
    agent_findings: Annotated[List[Dict], operator.add]
    
    # Synthesis output
    synthesized_finding: Optional[str]
    final_confidence: float
    consensus_reached: bool


# ============================================================================
# Swarm Nodes
# ============================================================================

@traceable(name="swarm_dispatcher")
async def dispatch_to_agents(state: SwarmState) -> List[Send]:
    """
    Dispatch investigation to assigned agents.
    
    Uses Send API to dynamically create parallel branches.
    """
    sends = []
    
    for agent_id in state["assigned_agents"]:
        # Create a Send for each agent
        sends.append(
            Send(
                "agent_investigate",
                {
                    **state,
                    "current_agent": agent_id
                }
            )
        )
    
    return sends


@traceable(name="agent_investigation")
async def agent_investigate(state: Dict) -> Dict:
    """
    Individual agent investigation.
    
    Each agent runs its own harness loop and returns findings.
    """
    agent_id = state["current_agent"]
    
    # Get agent instance
    agent = get_agent_by_id(agent_id)
    
    # Create harness graph for this agent
    harness = create_harness_graph(agent)
    
    # Run investigation
    initial_state = create_initial_state(
        ticket_id=state["ticket_id"],
        ticket_description=state["ticket_description"],
        ticket_severity=state["ticket_severity"],
        agent_id=agent_id,
        execution_mode="single_agent"
    )
    
    result = await harness.ainvoke(initial_state)
    
    return {
        "agent_findings": [{
            "agent_id": agent_id,
            "finding": result.get("finding"),
            "confidence": result.get("current_confidence", 0),
            "hypotheses": [h.dict() for h in result.get("hypotheses", [])],
            "observations": [o.dict() for o in result.get("observations", [])]
        }]
    }


@traceable(name="swarm_synthesizer")
async def synthesize_findings(state: SwarmState) -> Dict:
    """
    Synthesize findings from all agents.
    
    Creates a unified conclusion from multiple perspectives.
    """
    findings = state["agent_findings"]
    
    # Check for consensus
    high_confidence = [f for f in findings if f["confidence"] >= 0.8]
    
    if len(high_confidence) >= 2:
        # Multiple agents agree - synthesize
        prompt = f"""Multiple specialist agents investigated this issue:

{findings}

Synthesize their findings into a unified conclusion.
Identify where agents agree and disagree.
Provide a final confidence score."""

        llm = ChatAnthropic(model="claude-sonnet-4-20250514")
        result = await llm.ainvoke(prompt)
        
        # Parse synthesis
        synthesis = parse_synthesis(result.content)
        
        return {
            "synthesized_finding": synthesis["finding"],
            "final_confidence": synthesis["confidence"],
            "consensus_reached": True
        }
    else:
        # No consensus - escalate
        return {
            "synthesized_finding": None,
            "final_confidence": max(f["confidence"] for f in findings),
            "consensus_reached": False
        }


# ============================================================================
# Swarm Graph Assembly
# ============================================================================

def create_swarm_graph(checkpointer=None):
    """Create the swarm coordination graph."""
    
    graph = StateGraph(SwarmState)
    
    # Add nodes
    graph.add_node("dispatch", dispatch_to_agents)
    graph.add_node("agent_investigate", agent_investigate)
    graph.add_node("synthesize", synthesize_findings)
    
    # Dispatch fans out to agents
    graph.add_edge(START, "dispatch")
    
    # Agent investigations converge at synthesize
    graph.add_edge("agent_investigate", "synthesize")
    
    # Synthesize ends the graph
    graph.add_edge("synthesize", END)
    
    return graph.compile(checkpointer=checkpointer)
```

### Agent Selection Logic

```python
"""
Agent Selection for Swarm Mode

Determines which agents to activate based on ticket characteristics.
"""

from typing import List, Set


AGENT_CAPABILITIES = {
    "log_agent": {
        "keywords": ["error", "exception", "log", "crash", "failure"],
        "severity_weight": {"critical": 1.0, "high": 0.9, "medium": 0.7, "low": 0.5}
    },
    "code_agent": {
        "keywords": ["bug", "code", "deploy", "release", "regression"],
        "severity_weight": {"critical": 0.8, "high": 0.9, "medium": 1.0, "low": 0.8}
    },
    "infra_agent": {
        "keywords": ["timeout", "latency", "memory", "cpu", "disk", "network"],
        "severity_weight": {"critical": 1.0, "high": 0.95, "medium": 0.7, "low": 0.4}
    },
    "db_agent": {
        "keywords": ["database", "query", "slow", "connection", "deadlock"],
        "severity_weight": {"critical": 0.9, "high": 0.85, "medium": 0.8, "low": 0.6}
    },
    "security_agent": {
        "keywords": ["auth", "permission", "access", "denied", "unauthorized"],
        "severity_weight": {"critical": 1.0, "high": 0.9, "medium": 0.6, "low": 0.3}
    }
}


def select_agents_for_ticket(
    ticket_description: str,
    ticket_severity: str,
    mode: str,
    max_agents: int = 5
) -> List[str]:
    """
    Select agents based on ticket content and mode.
    
    Args:
        ticket_description: The ticket text
        ticket_severity: Severity level
        mode: Execution mode (micro_swarm, full_swarm)
        max_agents: Maximum agents to select
        
    Returns:
        List of agent IDs to activate
    """
    description_lower = ticket_description.lower()
    scores = {}
    
    for agent_id, config in AGENT_CAPABILITIES.items():
        # Keyword matching
        keyword_matches = sum(
            1 for kw in config["keywords"]
            if kw in description_lower
        )
        
        # Severity weighting
        severity_weight = config["severity_weight"].get(ticket_severity, 0.5)
        
        # Combined score
        scores[agent_id] = keyword_matches * severity_weight
    
    # Sort by score
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # Select based on mode
    if mode == "micro_swarm":
        # Top 2-3 agents
        return [agent_id for agent_id, score in ranked[:3] if score > 0]
    elif mode == "full_swarm":
        # All relevant agents up to max
        return [agent_id for agent_id, score in ranked[:max_agents] if score > 0]
    else:
        # Single agent - top scorer
        return [ranked[0][0]] if ranked else ["log_agent"]
```

---

## Chapter 7: Context Engineering Integration

### Multi-Layer Context Architecture

Context is injected at multiple layers to optimize token usage and relevance.

```python
"""
Context Engineering for HACI on LangSmith

Implements the multi-layer context injection pattern:
- Layer 1: Foundational (system prompts, capabilities)
- Layer 2: Situational (ticket, customer context)
- Layer 3: Operational (investigation state)
- Layer 4: Dynamic (retrieved knowledge, RAG)
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from langsmith import traceable


@dataclass
class ContextBudget:
    """Token budget allocation for context layers."""
    total_tokens: int = 100000
    layer_1_foundational: int = 5000
    layer_2_situational: int = 10000
    layer_3_operational: int = 15000
    layer_4_dynamic: int = 20000
    response_reserve: int = 10000
    
    @property
    def available_for_dynamic(self) -> int:
        """Remaining tokens after fixed layers."""
        used = (
            self.layer_1_foundational +
            self.layer_2_situational +
            self.layer_3_operational +
            self.response_reserve
        )
        return self.total_tokens - used


@dataclass
class ContextLayer:
    """A single context layer with content and metadata."""
    name: str
    content: str
    priority: int
    token_count: int
    source: str


class ContextAssembler:
    """
    Assembles multi-layer context for agent prompts.
    
    Manages token budgets and prioritization across layers.
    """
    
    def __init__(self, budget: ContextBudget = None):
        self.budget = budget or ContextBudget()
        self.layers: Dict[str, ContextLayer] = {}
    
    @traceable(name="assemble_context")
    def assemble(
        self,
        state: HarnessState,
        agent: BaseAgent,
        include_dynamic: bool = True
    ) -> str:
        """
        Assemble complete context for an agent invocation.
        
        Returns formatted context string within budget.
        """
        sections = []
        
        # Layer 1: Foundational
        foundational = self._build_foundational(agent)
        sections.append(f"## Agent Capabilities\n{foundational}")
        
        # Layer 2: Situational
        situational = self._build_situational(state)
        sections.append(f"## Current Situation\n{situational}")
        
        # Layer 3: Operational
        operational = self._build_operational(state)
        sections.append(f"## Investigation State\n{operational}")
        
        # Layer 4: Dynamic (if enabled and budget allows)
        if include_dynamic:
            dynamic = self._build_dynamic(state)
            if dynamic:
                sections.append(f"## Retrieved Knowledge\n{dynamic}")
        
        return "\n\n".join(sections)
    
    def _build_foundational(self, agent: BaseAgent) -> str:
        """Layer 1: Agent identity and capabilities."""
        return f"""Agent: {agent.agent_id}
Tools Available: {', '.join(t.name for t in agent.tools)}
Specialization: {agent.specialization}

{agent.system_prompt}"""
    
    def _build_situational(self, state: HarnessState) -> str:
        """Layer 2: Ticket and customer context."""
        customer = state.get("customer_context", {})
        
        return f"""Ticket ID: {state['ticket_id']}
Severity: {state['ticket_severity']}
Description: {state['ticket_description']}

Customer: {customer.get('name', 'Unknown')}
Tier: {customer.get('tier', 'standard')}
Environment: {customer.get('environment', 'unknown')}"""
    
    def _build_operational(self, state: HarnessState) -> str:
        """Layer 3: Current investigation state."""
        hypotheses = state.get("hypotheses", [])
        observations = state.get("observations", [])
        
        hyp_summary = "\n".join([
            f"- {h.description} (confidence: {h.confidence:.0%})"
            for h in hypotheses[-3:]  # Last 3 hypotheses
        ]) or "None yet"
        
        obs_summary = "\n".join([
            f"- {o.finding}"
            for o in observations[-5:]  # Last 5 observations
        ]) or "None yet"
        
        return f"""Iteration: {state['iteration_count']} / {state['max_iterations']}
Current Phase: {state['current_phase']}
Confidence: {state.get('current_confidence', 0):.0%}

Recent Hypotheses:
{hyp_summary}

Recent Observations:
{obs_summary}

Identified Gaps: {', '.join(state.get('gaps', [])) or 'None'}"""
    
    def _build_dynamic(self, state: HarnessState) -> Optional[str]:
        """Layer 4: Retrieved knowledge from RAG."""
        # This would integrate with a vector store
        # For now, return placeholder
        return None
```

### Context Injection in Nodes

```python
"""
Using Context Assembler in Graph Nodes
"""

@traceable(name="think_with_context")
async def think_node_with_context(
    state: HarnessState,
    agent: BaseAgent,
    context_assembler: ContextAssembler
) -> Dict:
    """
    THINK phase with full context injection.
    """
    # Assemble context
    full_context = context_assembler.assemble(state, agent)
    
    # Build prompt with context
    prompt = f"""{full_context}

---

Based on the above context, analyze the situation and:
1. Form hypotheses about the root cause
2. Create an investigation plan

Respond in the required JSON format."""
    
    # Get response
    response = await agent.llm.ainvoke(prompt)
    
    return parse_think_response(response.content)
```

---

## Chapter 8: Human-in-the-Loop Patterns

### LangGraph Interrupt Mechanism

LangGraph provides native support for human-in-the-loop via interrupts.

```python
"""
Human-in-the-Loop with LangGraph Interrupts

Implements approval workflows using:
- interrupt_before: Pause before executing a node
- interrupt_after: Pause after a node completes
- Dynamic interrupts: Runtime decision to pause
"""

from langgraph.graph import StateGraph
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.types import interrupt, Command


# Compile graph with interrupt points
workflow = graph.compile(
    checkpointer=PostgresSaver.from_conn_string(DATABASE_URL),
    interrupt_before=["execute_action"],  # Pause before actions
    interrupt_after=["human_gate"]          # Pause after gate
)
```

### Human Approval Gate

```python
"""
Human Approval Gate Node

Implements risk-based approval requirements.
"""

from enum import Enum
from pydantic import BaseModel


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ApprovalRequest(BaseModel):
    """Request for human approval."""
    action: str
    risk_level: RiskLevel
    rationale: str
    timeout_minutes: int = 30
    auto_approve_if_timeout: bool = False


class HumanDecision(BaseModel):
    """Human's decision on approval request."""
    approved: bool
    feedback: Optional[str] = None
    modified_action: Optional[str] = None
    decided_by: str
    decided_at: str


@traceable(name="human_gate")
async def human_gate_node(state: HarnessState) -> Dict:
    """
    Human approval gate with risk assessment.
    """
    # Assess risk level
    risk = assess_risk_level(state)
    
    # Check if auto-approve is allowed
    if can_auto_approve(state, risk):
        return {
            "approval_status": "approved",
            "human_feedback": "Auto-approved based on risk assessment"
        }
    
    # Create approval request
    request = ApprovalRequest(
        action=state.get("finding", "Proposed action"),
        risk_level=risk,
        rationale=build_rationale(state),
        timeout_minutes=get_timeout_for_risk(risk)
    )
    
    # Interrupt for human decision
    decision = interrupt({
        "type": "approval_request",
        "request": request.dict(),
        "state_summary": summarize_state(state)
    })
    
    # Process human decision
    return {
        "approval_status": "approved" if decision["approved"] else "rejected",
        "human_feedback": decision.get("feedback")
    }


def assess_risk_level(state: HarnessState) -> RiskLevel:
    """
    Assess risk level based on state.
    """
    severity = state["ticket_severity"]
    confidence = state.get("current_confidence", 0)
    mode = state["execution_mode"]
    
    # Critical severity = critical risk
    if severity == "critical":
        return RiskLevel.CRITICAL
    
    # Low confidence = high risk
    if confidence < 0.7:
        return RiskLevel.HIGH
    
    # Human-led mode = always high
    if mode == "human_led":
        return RiskLevel.HIGH
    
    # Default mapping
    risk_map = {
        "high": RiskLevel.MEDIUM,
        "medium": RiskLevel.LOW,
        "low": RiskLevel.LOW
    }
    return risk_map.get(severity, RiskLevel.MEDIUM)


def can_auto_approve(state: HarnessState, risk: RiskLevel) -> bool:
    """
    Determine if auto-approval is allowed.
    """
    # Never auto-approve critical or high risk
    if risk in [RiskLevel.CRITICAL, RiskLevel.HIGH]:
        return False
    
    # Check confidence threshold
    confidence = state.get("current_confidence", 0)
    if confidence < 0.9:
        return False
    
    # Check execution mode
    if state["execution_mode"] == "human_led":
        return False
    
    # Check customer requirements
    customer = state.get("customer_context", {})
    if customer.get("requires_approval", False):
        return False
    
    return True
```

### Resuming After Approval

```python
"""
Resuming workflow after human approval.
"""

from langgraph.types import Command


async def handle_approval_response(
    thread_id: str,
    decision: HumanDecision,
    workflow: CompiledGraph
):
    """
    Resume workflow with human decision.
    """
    config = {"configurable": {"thread_id": thread_id}}
    
    # Resume with the decision
    result = await workflow.ainvoke(
        Command(resume=decision.model_dump()),
        config=config
    )
    
    return result


# FastAPI endpoint example
@app.post("/approvals/{thread_id}/approve")
async def approve_action(
    thread_id: str,
    feedback: Optional[str] = None
):
    decision = HumanDecision(
        approved=True,
        feedback=feedback,
        decided_by=current_user.id,
        decided_at=datetime.utcnow().isoformat()
    )
    
    result = await handle_approval_response(thread_id, decision, workflow)
    return {"status": "resumed", "result": result}


@app.post("/approvals/{thread_id}/reject")
async def reject_action(
    thread_id: str,
    feedback: str
):
    decision = HumanDecision(
        approved=False,
        feedback=feedback,
        decided_by=current_user.id,
        decided_at=datetime.utcnow().isoformat()
    )
    
    result = await handle_approval_response(thread_id, decision, workflow)
    return {"status": "rejected", "result": result}
```

### Risk Assessment Criteria

| Risk Level | Criteria | Approval Required | Timeout |
|------------|----------|-------------------|---------|
| **LOW** | Read-only operations, ≥90% confidence | Auto-approved | N/A |
| **MEDIUM** | Reversible changes, 70-90% confidence | Optional (15 min) | 15 min |
| **HIGH** | Production impact, <70% confidence | Required | 30 min |
| **CRITICAL** | Irreversible, customer-impacting, security | Required + Escalation | 60 min |

---

## Chapter 9: Testing & Evaluation

### Testing Pyramid

```
                    ┌────────────────────┐
                    │   E2E Agent Tests  │  ← Full workflow validation
                    └────────┬───────────┘
                   ┌─────────┴──────────┐
                   │ Integration Tests  │    ← Multi-agent, tools, state
                   └─────────┬──────────┘
          ┌──────────────────┴────────────────────┐
          │            Unit Tests                  │  ← Individual nodes/phases
          └────────────────────────────────────────┘
```

### Unit Testing Harness Phases

```python
"""
Unit Tests for HACI Harness Phases

Tests individual nodes in isolation with mocked dependencies.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.graphs.harness_graph import think_node, act_node, observe_node, evaluate_node


@pytest.fixture
def initial_state():
    """Create initial state for testing."""
    return {
        "ticket_id": "TEST-001",
        "ticket_description": "Application returning 500 errors",
        "ticket_severity": "high",
        "execution_mode": "single_agent",
        "max_iterations": 5,
        "confidence_threshold": 0.8,
        "hypotheses": [],
        "observations": [],
        "tool_calls": [],
        "iteration_count": 0,
        "current_phase": "think",
        "gaps": []
    }


@pytest.fixture
def mock_llm_response():
    """Mock LLM response."""
    return {
        "hypotheses": [
            {
                "id": "hyp_1",
                "description": "Database connection pool exhausted",
                "confidence": 0.6
            }
        ],
        "investigation_plan": [
            {
                "tool": "search_logs",
                "purpose": "Find connection errors",
                "arguments": {"query": "connection pool"},
                "priority": 1
            }
        ]
    }


class TestThinkNode:
    """Tests for THINK phase."""
    
    @pytest.mark.asyncio
    async def test_generates_hypotheses(self, initial_state, mock_llm_response):
        """THINK should generate at least one hypothesis."""
        agent = MagicMock()
        agent.think = AsyncMock(return_value=mock_llm_response)
        
        result = await think_node(initial_state, agent)
        
        assert len(result["hypotheses"]) > 0
        assert result["current_phase"] == "act"
    
    @pytest.mark.asyncio
    async def test_creates_investigation_plan(self, initial_state, mock_llm_response):
        """THINK should create a non-empty investigation plan."""
        agent = MagicMock()
        agent.think = AsyncMock(return_value=mock_llm_response)
        
        result = await think_node(initial_state, agent)
        
        assert len(result["investigation_plan"]) > 0
        assert all("tool" in step for step in result["investigation_plan"])


class TestActNode:
    """Tests for ACT phase."""
    
    @pytest.mark.asyncio
    async def test_executes_tools(self, initial_state):
        """ACT should execute all tools in plan."""
        state = {
            **initial_state,
            "investigation_plan": [
                {"tool": "search_logs", "arguments": {"query": "error"}}
            ]
        }
        
        agent = MagicMock()
        agent.act = AsyncMock(return_value=[
            {"tool_name": "search_logs", "result": "Found 10 errors"}
        ])
        
        result = await act_node(state, agent)
        
        assert len(result["tool_calls"]) == 1
        assert result["current_phase"] == "observe"
    
    @pytest.mark.asyncio
    async def test_handles_tool_errors_gracefully(self, initial_state):
        """ACT should capture tool errors without failing."""
        state = {
            **initial_state,
            "investigation_plan": [
                {"tool": "failing_tool", "arguments": {}}
            ]
        }
        
        agent = MagicMock()
        agent.act = AsyncMock(return_value=[
            {"tool_name": "failing_tool", "result": None, "error": "Tool failed"}
        ])
        
        result = await act_node(state, agent)
        
        assert result["tool_calls"][0]["error"] is not None


class TestEvaluateNode:
    """Tests for EVALUATE phase."""
    
    @pytest.mark.asyncio
    async def test_completes_when_confident(self, initial_state):
        """EVALUATE should complete when confidence exceeds threshold."""
        state = {
            **initial_state,
            "hypotheses": [
                MagicMock(confidence=0.95, description="Root cause found")
            ],
            "current_confidence": 0.95
        }
        
        agent = MagicMock()
        agent.evaluate = AsyncMock(return_value={
            "confidence": 0.95,
            "decision": "complete",
            "finding": "Root cause found"
        })
        
        result = await evaluate_node(state, agent)
        
        assert result["decision"] == "complete"
    
    @pytest.mark.asyncio
    async def test_escalates_on_max_iterations(self, initial_state):
        """EVALUATE should escalate when max iterations reached."""
        state = {
            **initial_state,
            "iteration_count": 5,
            "max_iterations": 5,
            "hypotheses": [MagicMock(confidence=0.5)]
        }
        
        agent = MagicMock()
        agent.evaluate = AsyncMock(return_value={
            "confidence": 0.5,
            "decision": "escalate",
            "escalation_reason": "Max iterations reached"
        })
        
        result = await evaluate_node(state, agent)
        
        assert result["decision"] == "escalate"
```

### LangSmith Datasets and Evaluators

```python
"""
LangSmith Evaluation Setup

Create datasets and custom evaluators for HACI.
"""

from langsmith import Client
from langsmith.evaluation import evaluate, LangChainStringEvaluator


client = Client()


# Create evaluation dataset
dataset = client.create_dataset(
    dataset_name="haci-support-tickets-v1",
    description="Support tickets for HACI evaluation"
)

# Add examples
examples = [
    {
        "inputs": {
            "ticket_content": "Application throwing 500 errors after deployment",
            "severity": "high",
            "customer_tier": "enterprise"
        },
        "expected_output": {
            "root_cause_category": "deployment_issue",
            "expected_tools": ["search_logs", "get_deployments"],
            "min_confidence": 0.8,
            "requires_human_approval": True
        }
    },
    {
        "inputs": {
            "ticket_content": "Database queries timing out",
            "severity": "critical",
            "customer_tier": "standard"
        },
        "expected_output": {
            "root_cause_category": "database_performance",
            "expected_tools": ["query_metrics", "get_slow_queries"],
            "min_confidence": 0.85,
            "requires_human_approval": True
        }
    }
]

for example in examples:
    client.create_example(
        dataset_id=dataset.id,
        inputs=example["inputs"],
        outputs=example["expected_output"]
    )


# Custom evaluators
def root_cause_accuracy(run, example) -> dict:
    """Check if identified root cause category matches expected."""
    predicted = run.outputs.get("root_cause_category")
    expected = example.outputs.get("root_cause_category")
    
    return {
        "key": "root_cause_accuracy",
        "score": 1.0 if predicted == expected else 0.0
    }


def tool_selection_score(run, example) -> dict:
    """Evaluate tool selection overlap with expected tools."""
    predicted_tools = set(run.outputs.get("tools_used", []))
    expected_tools = set(example.outputs.get("expected_tools", []))
    
    if not expected_tools:
        return {"key": "tool_selection", "score": 1.0}
    
    intersection = predicted_tools & expected_tools
    union = predicted_tools | expected_tools
    
    jaccard = len(intersection) / len(union) if union else 0
    
    return {
        "key": "tool_selection",
        "score": jaccard
    }


def confidence_calibration(run, example) -> dict:
    """Check if confidence is appropriate for the result."""
    confidence = run.outputs.get("confidence", 0)
    correct = run.outputs.get("root_cause_category") == example.outputs.get("root_cause_category")
    
    # Penalize high confidence when wrong
    if not correct and confidence > 0.8:
        return {"key": "confidence_calibration", "score": 0.0}
    
    # Penalize low confidence when right
    if correct and confidence < 0.5:
        return {"key": "confidence_calibration", "score": 0.5}
    
    return {"key": "confidence_calibration", "score": 1.0}


# Run evaluation
results = evaluate(
    haci_agent_target,  # Your agent function
    data="haci-support-tickets-v1",
    evaluators=[
        root_cause_accuracy,
        tool_selection_score,
        confidence_calibration
    ],
    experiment_prefix="haci-eval",
    max_concurrency=4
)
```

### CI/CD Integration

```yaml
# .github/workflows/haci-eval.yml
name: HACI Evaluation

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio
      
      - name: Run unit tests
        run: pytest tests/unit -v
      
      - name: Run LangSmith evaluation
        env:
          LANGCHAIN_API_KEY: ${{ secrets.LANGCHAIN_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python scripts/run_evaluation.py
      
      - name: Check evaluation thresholds
        run: |
          python -c "
          from langsmith import Client
          client = Client()
          
          # Get latest experiment
          experiments = list(client.list_projects(
              project_name_contains='haci-eval'
          ))
          
          if experiments:
              latest = experiments[0]
              # Check metrics meet thresholds
              assert latest.feedback_stats.get('root_cause_accuracy', 0) >= 0.9
              assert latest.feedback_stats.get('tool_selection', 0) >= 0.85
              print('✅ All thresholds met')
          "
```

---

## Chapter 10: Production Deployment

### Deployment Options

| Option | Pros | Cons | Best For |
|--------|------|------|----------|
| **LangGraph Platform** | Managed, zero infrastructure | Less control | Quick deployment |
| **Self-Hosted Docker** | Full control, custom infrastructure | More maintenance | Enterprise requirements |
| **Serverless** | Pay per invocation | Cold starts | Variable load |

### LangGraph Platform Deployment

```json
// langgraph.json
{
  "graphs": {
    "haci_harness": "./src/graphs/harness_graph.py:create_harness_graph",
    "haci_swarm": "./src/graphs/swarm_graph.py:create_swarm_graph"
  },
  "dependencies": ["."],
  "env": ".env"
}
```

```bash
# Deploy to LangGraph Platform
langgraph build
langgraph deploy --name haci-production
```

### Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY main.py .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  haci-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LANGCHAIN_API_KEY=${LANGCHAIN_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - DATABASE_URL=postgresql://haci:password@postgres:5432/haci
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2'
          memory: 4G

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: haci
      POSTGRES_USER: haci
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U haci"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:
```

### FastAPI Production Server

```python
"""
Production FastAPI Server for HACI

main.py - Entry point for the HACI API
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import uuid

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.types import Command

from src.graphs.harness_graph import create_harness_graph
from src.agents.log_agent import LogAgent


app = FastAPI(
    title="HACI API",
    description="Harness-Enhanced Agentic Collaborative Intelligence",
    version="1.0.0"
)


# Initialize components
checkpointer = PostgresSaver.from_conn_string(os.environ["DATABASE_URL"])
agent = LogAgent()
workflow = create_harness_graph(agent, checkpointer)


class TicketRequest(BaseModel):
    ticket_id: str
    description: str
    severity: str = "medium"
    customer_context: Optional[dict] = None


class TicketResponse(BaseModel):
    thread_id: str
    status: str
    finding: Optional[str] = None
    confidence: Optional[float] = None
    requires_approval: bool = False


@app.post("/tickets/investigate", response_model=TicketResponse)
async def investigate_ticket(request: TicketRequest):
    """Start an investigation for a support ticket."""
    thread_id = str(uuid.uuid4())
    
    initial_state = {
        "ticket_id": request.ticket_id,
        "ticket_description": request.description,
        "ticket_severity": request.severity,
        "customer_context": request.customer_context,
        "execution_mode": "single_agent",
        "agent_id": "log_agent",
        "max_iterations": 10,
        "confidence_threshold": 0.80,
        "hypotheses": [],
        "observations": [],
        "tool_calls": [],
        "iteration_count": 0,
        "current_phase": "think",
        "gaps": []
    }
    
    config = {"configurable": {"thread_id": thread_id}}
    
    # Run investigation
    result = await workflow.ainvoke(initial_state, config)
    
    # Check if interrupted for approval
    state = await workflow.aget_state(config)
    if state.next:  # Graph is paused
        return TicketResponse(
            thread_id=thread_id,
            status="awaiting_approval",
            finding=result.get("finding"),
            confidence=result.get("current_confidence"),
            requires_approval=True
        )
    
    return TicketResponse(
        thread_id=thread_id,
        status=result.get("decision", "complete"),
        finding=result.get("finding"),
        confidence=result.get("current_confidence"),
        requires_approval=False
    )


@app.post("/tickets/{thread_id}/approve")
async def approve_action(thread_id: str, feedback: Optional[str] = None):
    """Approve a pending action."""
    config = {"configurable": {"thread_id": thread_id}}
    
    decision = {
        "approved": True,
        "feedback": feedback,
        "decided_at": datetime.utcnow().isoformat()
    }
    
    result = await workflow.ainvoke(
        Command(resume=decision),
        config=config
    )
    
    return {"status": "approved", "result": result.get("finding")}


@app.post("/tickets/{thread_id}/reject")
async def reject_action(thread_id: str, reason: str):
    """Reject a pending action."""
    config = {"configurable": {"thread_id": thread_id}}
    
    decision = {
        "approved": False,
        "feedback": reason,
        "decided_at": datetime.utcnow().isoformat()
    }
    
    result = await workflow.ainvoke(
        Command(resume=decision),
        config=config
    )
    
    return {"status": "rejected", "escalated": True}


@app.get("/tickets/{thread_id}/status")
async def get_status(thread_id: str):
    """Get current investigation status."""
    config = {"configurable": {"thread_id": thread_id}}
    
    state = await workflow.aget_state(config)
    
    return {
        "thread_id": thread_id,
        "phase": state.values.get("current_phase"),
        "iteration": state.values.get("iteration_count"),
        "confidence": state.values.get("current_confidence"),
        "awaiting_approval": bool(state.next)
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}
```

### Kubernetes Deployment

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: haci-api
  labels:
    app: haci
spec:
  replicas: 3
  selector:
    matchLabels:
      app: haci
  template:
    metadata:
      labels:
        app: haci
    spec:
      containers:
      - name: haci
        image: haci:latest
        ports:
        - containerPort: 8000
        env:
        - name: LANGCHAIN_API_KEY
          valueFrom:
            secretKeyRef:
              name: haci-secrets
              key: langchain-api-key
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: haci-secrets
              key: anthropic-api-key
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: haci-secrets
              key: database-url
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: haci-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: haci-api
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Production Monitoring

```python
"""
Production Monitoring with Prometheus Metrics
"""

from prometheus_client import Counter, Histogram, Gauge
import structlog


# Metrics
TICKETS_PROCESSED = Counter(
    'haci_tickets_processed_total',
    'Total tickets processed',
    ['severity', 'outcome']
)

INVESTIGATION_DURATION = Histogram(
    'haci_investigation_duration_seconds',
    'Investigation duration in seconds',
    buckets=[1, 5, 10, 30, 60, 120, 300]
)

CONFIDENCE_SCORE = Histogram(
    'haci_confidence_score',
    'Final confidence scores',
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)

PENDING_APPROVALS = Gauge(
    'haci_pending_approvals',
    'Number of investigations awaiting approval'
)


# Structured logging
logger = structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
```

### Production Readiness Checklist

**Security:**
- [ ] API keys in secrets manager
- [ ] TLS/HTTPS enabled
- [ ] Rate limiting configured
- [ ] Authentication/authorization
- [ ] Input validation

**Observability:**
- [ ] LangSmith tracing enabled
- [ ] Prometheus metrics exposed
- [ ] Structured logging configured
- [ ] Health check endpoints
- [ ] Alerting rules defined

**Reliability:**
- [ ] PostgreSQL checkpointer for state
- [ ] Auto-scaling configured
- [ ] Connection pooling enabled
- [ ] Graceful shutdown handling
- [ ] Circuit breakers for external calls

**Testing:**
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] E2E tests in staging
- [ ] LangSmith evaluation datasets
- [ ] CI/CD pipeline configured
- [ ] Performance baseline established

---

## Summary

This guide covered the complete implementation of HACI on LangSmith:

1. **Setup** - Environment configuration and project structure
2. **Graph Architecture** - State schema and LangGraph design
3. **Agent Implementation** - Specialist agents with tool binding
4. **Observability** - Comprehensive tracing and monitoring
5. **Harness Phases** - THINK→ACT→OBSERVE→EVALUATE deep dive
6. **Swarm Coordination** - Multi-agent parallel execution
7. **Context Engineering** - Multi-layer context injection
8. **Human-in-the-Loop** - Approval workflows and interrupts
9. **Testing & Evaluation** - Unit tests and LangSmith datasets
10. **Deployment** - Docker, Kubernetes, and production setup

For more information:
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Anthropic Documentation](https://docs.anthropic.com/)

---

*HACI Implementation Guide - Built for enterprise-grade AI automation with calibrated autonomy and human oversight.*
