# HACI Architecture

This directory contains the architectural documentation for HACI (Harness-Enhanced Agentic Collaborative Intelligence).

## Contents

| Document | Description |
|----------|-------------|
| [overview.md](overview.md) | High-level system architecture |
| [context-engineering.md](context-engineering.md) | Multi-agent memory management |
| [execution-modes.md](execution-modes.md) | Detailed execution mode specifications |
| [harness-pattern.md](harness-pattern.md) | The core harness pattern implementation |
| [agents.md](agents.md) | Specialized agent specifications |
| [adr/](adr/) | Architecture Decision Records |

## Architecture Overview

HACI is organized into four distinct layers:

```
┌─────────────────────────────────────────────────────────────┐
│                 LAYER 4: META-ORCHESTRATION                  │
│  • Complexity scoring                                        │
│  • Execution mode selection                                  │
│  • Resource management                                       │
│  • Cost optimization                                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│           LAYER 3: HUMAN-AGENT COLLABORATION                 │
│  • Confidence-based action gating                            │
│  • Approval workflows                                        │
│  • Human escalation paths                                    │
│  • Review mechanisms                                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              LAYER 2: SWARM INTELLIGENCE                     │
│  • Context Bus (shared state)                                │
│  • Agent coordination                                        │
│  • Dispute resolution                                        │
│  • Finding consolidation                                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  LAYER 1: FOUNDATION                         │
│  • Specialized agents                                        │
│  • Harness pattern                                           │
│  • Tool integrations (API + MCP)                             │
│  • LLM providers                                             │
└─────────────────────────────────────────────────────────────┘
```

## Key Concepts

### The Harness Pattern

The "harness" is the central middleware that wraps all agent operations, providing:

- **Credential management** - Secure injection of API keys and tokens
- **Audit logging** - Complete trail of all agent actions
- **Rate limiting** - Protection against runaway operations
- **Approval gates** - Human intervention points based on confidence

### Execution Modes

| Mode | Agents | Use Case | Human Oversight |
|------|--------|----------|-----------------|
| Single Agent | 1 | Simple, well-defined tasks | Minimal |
| Micro-Swarm | 2-3 | Multi-domain coordination | Checkpoint-based |
| Full Swarm | 4+ | Complex, high-stakes issues | Active monitoring |
| Human-Led | Variable | Critical/sensitive matters | Direct control |

### Confidence-Based Gating

Actions are gated based on agent confidence:

| Confidence | Action |
|------------|--------|
| ≥ 95% | Auto-execute |
| 85-94% | Execute with post-review |
| 70-84% | Require human approval |
| < 70% | Human-led with AI assistance |

## Further Reading

- [Context Engineering Framework](context-engineering.md) - How agents manage memory
- [Integration Guide](../integration/README.md) - API and MCP integration
- [Governance Framework](../governance/README.md) - Compliance and risk management
