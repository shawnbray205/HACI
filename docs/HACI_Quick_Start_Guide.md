# HACI Quick Start Guide

> Get HACI running in 15 minutes and see AI-powered support automation in action

---

## What You'll Build

In this guide, you'll:
1. ✅ Set up a minimal HACI environment
2. ✅ Run your first automated investigation
3. ✅ See the THINK→ACT→OBSERVE→EVALUATE harness in action
4. ✅ Experience human-in-the-loop approval workflows

**Time:** 15 minutes  
**Prerequisites:** Docker, Python 3.11+, API key (Anthropic or OpenAI)

---

## Option A: Docker Quick Start (5 minutes)

The fastest way to see HACI in action.

### Step 1: Clone and Configure

```bash
# Clone the HACI starter kit
git clone https://github.com/your-org/haci-quickstart.git
cd haci-quickstart

# Copy environment template
cp .env.example .env
```

### Step 2: Add Your API Key

Edit `.env` and add your LLM provider key:

```bash
# Choose one (Anthropic recommended)
ANTHROPIC_API_KEY=sk-ant-your-key-here
# OR
OPENAI_API_KEY=sk-your-key-here
```

### Step 3: Launch HACI

```bash
docker-compose up -d
```

### Step 4: Open the Demo UI

Navigate to: **http://localhost:8080**

You'll see the HACI Investigation Dashboard. Click "Submit Test Ticket" to trigger your first investigation.

### Step 5: Watch the Magic

The dashboard shows real-time progress through:
- 🧠 **THINK** - Forming hypotheses
- ⚡ **ACT** - Querying mock monitoring tools
- 👁️ **OBSERVE** - Analyzing results
- ✅ **EVALUATE** - Determining confidence and next steps

**Congratulations!** You've just run your first HACI investigation.

---

## Option B: Python Quick Start (15 minutes)

For developers who want to understand the code.

### Step 1: Create Project

```bash
mkdir haci-demo && cd haci-demo
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install langgraph langchain-anthropic langsmith pydantic
```

### Step 3: Set Environment Variables

```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
export LANGCHAIN_TRACING_V2="true"  # Optional: enables LangSmith tracing
```

### Step 4: Create the Demo Script

Create `haci_demo.py`:

```python
"""
HACI Quick Start Demo
=====================
A minimal implementation showing the core harness pattern.
"""

import asyncio
from typing import TypedDict, Literal, Annotated, List
from langgraph.graph import StateGraph, START, END
from langchain_anthropic import ChatAnthropic
import operator


# =============================================================================
# STATE DEFINITION
# =============================================================================

class InvestigationState(TypedDict):
    """State that flows through the harness."""
    # Input
    ticket: str
    severity: str
    
    # Investigation progress
    hypotheses: Annotated[List[str], operator.add]
    actions_taken: Annotated[List[str], operator.add]
    observations: Annotated[List[str], operator.add]
    
    # Output
    confidence: float
    finding: str
    decision: Literal["continue", "complete", "escalate"]
    iteration: int


# =============================================================================
# LLM SETUP
# =============================================================================

llm = ChatAnthropic(model="claude-sonnet-4-20250514")


# =============================================================================
# HARNESS PHASE NODES
# =============================================================================

async def think_node(state: InvestigationState) -> dict:
    """🧠 THINK: Analyze the problem and form hypotheses."""
    print("\n🧠 THINK PHASE")
    print("-" * 40)
    
    prompt = f"""You are investigating a support ticket.

Ticket: {state['ticket']}
Severity: {state['severity']}
Previous observations: {state['observations']}

Form 1-2 hypotheses about what might be wrong.
Be specific and actionable. Reply with just the hypotheses, one per line."""

    response = await llm.ainvoke(prompt)
    hypotheses = [h.strip() for h in response.content.strip().split('\n') if h.strip()]
    
    print(f"Hypotheses formed:")
    for h in hypotheses:
        print(f"  → {h}")
    
    return {"hypotheses": hypotheses}


async def act_node(state: InvestigationState) -> dict:
    """⚡ ACT: Execute investigation actions (simulated tools)."""
    print("\n⚡ ACT PHASE")
    print("-" * 40)
    
    # Simulate tool calls based on hypotheses
    actions = []
    
    if any("log" in h.lower() or "error" in h.lower() for h in state['hypotheses']):
        actions.append("Searched error logs: Found 47 'ConnectionTimeout' errors in last hour")
    
    if any("database" in h.lower() or "db" in h.lower() for h in state['hypotheses']):
        actions.append("Checked DB metrics: Connection pool at 95% capacity, avg query time 2.3s")
    
    if any("deploy" in h.lower() or "release" in h.lower() for h in state['hypotheses']):
        actions.append("Checked deployments: Version 2.4.1 deployed 45 minutes ago")
    
    if any("memory" in h.lower() or "cpu" in h.lower() for h in state['hypotheses']):
        actions.append("Checked infrastructure: Memory usage 78%, CPU 45%, no anomalies")
    
    # Default action if no specific matches
    if not actions:
        actions.append("Ran general diagnostics: System health nominal, no obvious issues")
    
    print(f"Actions executed:")
    for a in actions:
        print(f"  → {a}")
    
    return {"actions_taken": actions}


async def observe_node(state: InvestigationState) -> dict:
    """👁️ OBSERVE: Analyze results and extract insights."""
    print("\n👁️ OBSERVE PHASE")
    print("-" * 40)
    
    prompt = f"""Based on these investigation results, what do you observe?

Hypotheses: {state['hypotheses']}
Actions & Results: {state['actions_taken']}

Provide 1-2 key observations. Be specific about what the data tells us."""

    response = await llm.ainvoke(prompt)
    observations = [response.content.strip()]
    
    print(f"Observations:")
    for o in observations:
        print(f"  → {o[:100]}..." if len(o) > 100 else f"  → {o}")
    
    return {"observations": observations}


async def evaluate_node(state: InvestigationState) -> dict:
    """✅ EVALUATE: Determine confidence and next action."""
    print("\n✅ EVALUATE PHASE")
    print("-" * 40)
    
    prompt = f"""Evaluate this investigation:

Ticket: {state['ticket']}
Hypotheses: {state['hypotheses']}
Evidence: {state['actions_taken']}
Observations: {state['observations']}
Iteration: {state['iteration']} of 3

Provide:
1. Confidence level (0.0 to 1.0) that you've found the root cause
2. Your finding (what's the root cause?)
3. Decision: "complete" if confidence >= 0.8, "continue" if more investigation needed, "escalate" if stuck

Format your response as:
CONFIDENCE: [number]
FINDING: [your finding]
DECISION: [complete/continue/escalate]"""

    response = await llm.ainvoke(prompt)
    content = response.content
    
    # Parse response
    confidence = 0.5
    finding = "Investigation in progress"
    decision = "continue"
    
    for line in content.split('\n'):
        if line.startswith('CONFIDENCE:'):
            try:
                confidence = float(line.split(':')[1].strip())
            except:
                pass
        elif line.startswith('FINDING:'):
            finding = line.split(':', 1)[1].strip()
        elif line.startswith('DECISION:'):
            decision = line.split(':')[1].strip().lower()
    
    # Force complete after max iterations
    if state['iteration'] >= 2 and decision == "continue":
        decision = "complete"
    
    print(f"Confidence: {confidence:.0%}")
    print(f"Finding: {finding[:80]}..." if len(finding) > 80 else f"Finding: {finding}")
    print(f"Decision: {decision.upper()}")
    
    return {
        "confidence": confidence,
        "finding": finding,
        "decision": decision,
        "iteration": state['iteration'] + 1
    }


# =============================================================================
# ROUTING LOGIC
# =============================================================================

def route_after_evaluate(state: InvestigationState) -> str:
    """Determine next step based on evaluation."""
    if state['decision'] == "complete":
        return "complete"
    elif state['decision'] == "escalate":
        return "escalate"
    else:
        return "think"  # Continue the loop


def complete_node(state: InvestigationState) -> dict:
    """Investigation completed successfully."""
    print("\n" + "=" * 50)
    print("🎉 INVESTIGATION COMPLETE")
    print("=" * 50)
    print(f"Root Cause: {state['finding']}")
    print(f"Confidence: {state['confidence']:.0%}")
    print(f"Iterations: {state['iteration']}")
    return {}


def escalate_node(state: InvestigationState) -> dict:
    """Escalate to human operator."""
    print("\n" + "=" * 50)
    print("🚨 ESCALATING TO HUMAN")
    print("=" * 50)
    print(f"Reason: Unable to reach confident conclusion")
    print(f"Current Finding: {state['finding']}")
    return {}


# =============================================================================
# GRAPH ASSEMBLY
# =============================================================================

def create_haci_graph():
    """Build the HACI harness graph."""
    graph = StateGraph(InvestigationState)
    
    # Add nodes
    graph.add_node("think", think_node)
    graph.add_node("act", act_node)
    graph.add_node("observe", observe_node)
    graph.add_node("evaluate", evaluate_node)
    graph.add_node("complete", complete_node)
    graph.add_node("escalate", escalate_node)
    
    # Add edges (the harness flow)
    graph.add_edge(START, "think")
    graph.add_edge("think", "act")
    graph.add_edge("act", "observe")
    graph.add_edge("observe", "evaluate")
    
    # Conditional routing after evaluate
    graph.add_conditional_edges(
        "evaluate",
        route_after_evaluate,
        {
            "think": "think",      # Loop back
            "complete": "complete", # Success
            "escalate": "escalate"  # Human needed
        }
    )
    
    graph.add_edge("complete", END)
    graph.add_edge("escalate", END)
    
    return graph.compile()


# =============================================================================
# MAIN EXECUTION
# =============================================================================

async def main():
    """Run the HACI demo."""
    print("=" * 50)
    print("   HACI Quick Start Demo")
    print("   Harness-Enhanced Agentic Collaborative Intelligence")
    print("=" * 50)
    
    # Create the graph
    graph = create_haci_graph()
    
    # Define a test ticket
    initial_state = {
        "ticket": "Users reporting slow page loads and occasional 500 errors since this morning's deployment",
        "severity": "high",
        "hypotheses": [],
        "actions_taken": [],
        "observations": [],
        "confidence": 0.0,
        "finding": "",
        "decision": "continue",
        "iteration": 0
    }
    
    print(f"\n📋 TICKET: {initial_state['ticket']}")
    print(f"🔴 SEVERITY: {initial_state['severity'].upper()}")
    print("\nStarting investigation...\n")
    
    # Run the investigation
    result = await graph.ainvoke(initial_state)
    
    print("\n" + "=" * 50)
    print("   FINAL REPORT")
    print("=" * 50)
    print(f"Status: {'RESOLVED' if result['decision'] == 'complete' else 'ESCALATED'}")
    print(f"Root Cause: {result['finding']}")
    print(f"Confidence: {result['confidence']:.0%}")
    print(f"Total Iterations: {result['iteration']}")
    print(f"Hypotheses Explored: {len(result['hypotheses'])}")
    print(f"Actions Taken: {len(result['actions_taken'])}")


if __name__ == "__main__":
    asyncio.run(main())
```

### Step 5: Run the Demo

```bash
python haci_demo.py
```

### Expected Output

```
==================================================
   HACI Quick Start Demo
   Harness-Enhanced Agentic Collaborative Intelligence
==================================================

📋 TICKET: Users reporting slow page loads and occasional 500 errors...
🔴 SEVERITY: HIGH

Starting investigation...

🧠 THINK PHASE
----------------------------------------
Hypotheses formed:
  → Database connection pool exhaustion causing timeouts
  → Recent deployment introduced performance regression

⚡ ACT PHASE
----------------------------------------
Actions executed:
  → Checked DB metrics: Connection pool at 95% capacity
  → Checked deployments: Version 2.4.1 deployed 45 minutes ago

👁️ OBSERVE PHASE
----------------------------------------
Observations:
  → Database connection pool near capacity correlates with deployment...

✅ EVALUATE PHASE
----------------------------------------
Confidence: 85%
Finding: Database connection pool exhaustion triggered by deployment
Decision: COMPLETE

==================================================
🎉 INVESTIGATION COMPLETE
==================================================
Root Cause: Database connection pool exhaustion caused by v2.4.1 deployment
Confidence: 85%
Iterations: 1
```

---

## What Just Happened?

You witnessed HACI's core **harness pattern**:

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  THINK   │────▶│   ACT    │────▶│ OBSERVE  │────▶│ EVALUATE │
│          │     │          │     │          │     │          │
│ Analyze  │     │ Execute  │     │ Extract  │     │ Decide   │
│ Form     │     │ Tools    │     │ Insights │     │ Next     │
│ Hypotheses│    │ Gather   │     │ Update   │     │ Action   │
└──────────┘     └──────────┘     └──────────┘     └────┬─────┘
      ▲                                                  │
      │                    ┌─────────────────────────────┤
      │                    │                             │
      │              ┌─────▼─────┐               ┌───────▼──────┐
      └──────────────│ CONTINUE  │               │   COMPLETE   │
                     │ (loop)    │               │  or ESCALATE │
                     └───────────┘               └──────────────┘
```

**Key Concepts Demonstrated:**

| Concept | What You Saw |
|---------|--------------|
| **Harness Loop** | Structured THINK→ACT→OBSERVE→EVALUATE cycle |
| **Hypothesis-Driven** | AI formed testable theories before acting |
| **Evidence-Based** | Actions gathered specific data to test hypotheses |
| **Confidence Scoring** | AI self-assessed certainty before concluding |
| **Bounded Autonomy** | Max iterations prevent infinite loops |

---

## Next Steps

### Try Different Scenarios

Modify the `initial_state` in the script:

```python
# Scenario 2: Security incident
initial_state = {
    "ticket": "Unauthorized API calls detected from unknown IP addresses",
    "severity": "critical",
    ...
}

# Scenario 3: Simple issue
initial_state = {
    "ticket": "User cannot reset password, getting 'invalid token' error",
    "severity": "low",
    ...
}
```

### Add Real Tools

Replace the simulated tool calls in `act_node` with real integrations:

```python
from langchain_community.tools import DatadogLogsSearchTool

# Real Datadog integration
datadog_tool = DatadogLogsSearchTool(api_key="your-key")
```

### Enable LangSmith Tracing

View every step in the LangSmith dashboard:

```bash
export LANGCHAIN_API_KEY="your-langsmith-key"
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_PROJECT="haci-demo"
```

Then run the demo and visit: https://smith.langchain.com

### Explore the Full Documentation

| Document | What You'll Learn |
|----------|-------------------|
| [LangSmith Implementation Guide](./HACI_LangSmith_Implementation_Guide.md) | Full 10-chapter implementation |
| [Technical Documentation](./HACI_Comprehensive_Technical_Documentation.md) | Complete architecture deep-dive |
| [Glossary](./HACI_Glossary.md) | All HACI terminology explained |
| [FAQ](./HACI_FAQ.md) | Common questions answered |

---

## Troubleshooting

### "No module named 'langgraph'"

```bash
pip install langgraph langchain-anthropic
```

### "Invalid API key"

Ensure your environment variable is set:
```bash
echo $ANTHROPIC_API_KEY  # Should show your key
```

### "Rate limit exceeded"

The demo makes ~4-8 LLM calls. If you hit rate limits:
- Wait 60 seconds and retry
- Use a different API key
- Switch to OpenAI: change `ChatAnthropic` to `ChatOpenAI`

### Docker won't start

```bash
# Check logs
docker-compose logs

# Reset and retry
docker-compose down -v
docker-compose up -d
```

---

## Getting Help

- 📧 **Email:** support@haci.ai
- 💬 **Discord:** discord.gg/haci
- 📖 **Docs:** docs.haci.ai
- 🐛 **Issues:** github.com/your-org/haci/issues

---

**You've completed the HACI Quick Start!** 🎉

You've seen the core harness pattern that powers enterprise-grade AI automation. The full HACI system adds:

- **10 specialized agents** (Log, Code, Infrastructure, Database, Security, etc.)
- **Multi-agent swarms** for complex issues
- **Human-in-the-loop approvals** for high-risk actions
- **50+ vendor integrations** (Datadog, PagerDuty, Jira, AWS, etc.)
- **Production observability** with LangSmith

Ready to go deeper? Check out the [full implementation guide](./HACI_LangSmith_Implementation_Guide.md).
