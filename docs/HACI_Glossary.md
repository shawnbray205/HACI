# HACI Glossary

> Comprehensive terminology reference for Harness-Enhanced Agentic Collaborative Intelligence

---

## Quick Reference

| Term | One-Line Definition |
|------|---------------------|
| **HACI** | AI automation system combining structured harness control with multi-agent collaboration |
| **Harness** | The THINK→ACT→OBSERVE→EVALUATE control loop that governs agent behavior |
| **Swarm** | Multiple specialist agents working in parallel on complex problems |
| **Confidence Score** | AI's self-assessed certainty (0-100%) determining autonomy level |
| **Human-in-the-Loop** | Approval gates where humans review/approve agent actions |

---

## Core Concepts

### HACI (Harness-Enhanced Agentic Collaborative Intelligence)

**Definition:** An enterprise AI automation platform that combines structured reasoning patterns (harness) with multi-agent collaboration (swarm) and calibrated human oversight.

**Key Characteristics:**
- Structured decision-making via the harness pattern
- Multi-agent coordination for complex problems
- Confidence-based autonomy scaling
- Built-in human approval workflows

**Example:** "HACI automatically investigated the outage, identified a database connection pool issue, and resolved it with 92% confidence—all within 8 minutes."

---

### Harness

**Definition:** The core control loop that governs how agents reason and act. Consists of four phases: THINK, ACT, OBSERVE, EVALUATE.

**Purpose:** Provides structure, predictability, and auditability to AI decision-making. Prevents unbounded or erratic agent behavior.

**Origin:** Inspired by the harness pattern from AI agent research, which constrains agent autonomy within defined boundaries.

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  THINK   │────▶│   ACT    │────▶│ OBSERVE  │────▶│ EVALUATE │
└──────────┘     └──────────┘     └──────────┘     └────┬─────┘
      ▲                                                  │
      └──────────────────── LOOP ────────────────────────┘
```

---

### Harness Phases

#### THINK Phase

**Definition:** The reasoning phase where the agent analyzes input, forms hypotheses, and creates an investigation plan.

**Activities:**
- Analyze ticket content and context
- Form testable hypotheses about root cause
- Prioritize investigation steps
- Plan which tools to invoke

**Output:** List of hypotheses + investigation plan

**Example:** "In the THINK phase, the agent hypothesized: (1) database connection pool exhaustion, (2) recent deployment regression, (3) upstream API timeout."

---

#### ACT Phase

**Definition:** The execution phase where the agent invokes tools to gather data and test hypotheses.

**Activities:**
- Execute planned tool calls
- Query monitoring systems
- Fetch logs, metrics, traces
- Interact with external systems

**Output:** Tool results and gathered evidence

**Example:** "During ACT, the agent queried Datadog for error logs, checked recent deployments in GitHub, and pulled database metrics from CloudWatch."

---

#### OBSERVE Phase

**Definition:** The analysis phase where the agent interprets tool results and extracts insights.

**Activities:**
- Parse and interpret tool outputs
- Identify patterns and correlations
- Update hypothesis confidence
- Note gaps in understanding

**Output:** Observations + updated confidence levels

**Example:** "The OBSERVE phase found that error rates spiked exactly when the deployment completed, correlating with connection pool warnings."

---

#### EVALUATE Phase

**Definition:** The decision phase where the agent determines next action based on accumulated evidence.

**Activities:**
- Calculate overall confidence
- Compare against thresholds
- Decide: continue, complete, escalate, or await human

**Output:** Decision + confidence score + (optional) finding

**Possible Decisions:**
| Decision | Meaning |
|----------|---------|
| `continue` | More investigation needed, loop back to THINK |
| `complete` | Confident in finding, end investigation |
| `escalate` | Cannot resolve, hand off to human |
| `await_human` | Need human approval before proceeding |

---

## Execution Modes

### Single Agent Mode

**Definition:** One specialist agent handles the entire investigation independently.

**When Used:** Simple, well-defined issues within one domain (e.g., log analysis only).

**Characteristics:**
- Fastest response time
- Lowest resource usage
- ~60% of tickets

**Example:** A straightforward "password reset not working" ticket handled by the Auth Agent alone.

---

### Micro-Swarm Mode

**Definition:** 2-3 specialist agents collaborate on a moderately complex issue.

**When Used:** Issues spanning 2-3 domains that benefit from parallel investigation.

**Characteristics:**
- Parallel investigation
- Cross-domain correlation
- ~25% of tickets

**Example:** API timeouts investigated by Log Agent + Infrastructure Agent + Code Agent simultaneously.

---

### Full Swarm Mode

**Definition:** 4+ specialist agents work in parallel with a coordinator synthesizing findings.

**When Used:** Complex, multi-faceted incidents requiring broad investigation.

**Characteristics:**
- Maximum parallelism
- Coordinator synthesizes findings
- Human checkpoint required
- ~14% of tickets

**Example:** Major outage investigated by Log, Code, Infrastructure, Database, and Security agents with Swarm Coordinator.

---

### Human-Led Mode

**Definition:** Human operator drives investigation with AI providing research assistance.

**When Used:** Novel situations, sensitive customers, regulatory requirements.

**Characteristics:**
- Human makes all decisions
- AI acts as research assistant
- Full audit trail
- ~1% of tickets

**Example:** Security incident for a healthcare customer requiring HIPAA compliance review.

---

## Agent Types

### Specialist Agent

**Definition:** An AI agent trained and tooled for a specific domain (logs, code, infrastructure, etc.).

**HACI Specialist Agents:**
| Agent | Domain | Primary Tools |
|-------|--------|---------------|
| Log Agent | Log analysis | Datadog, Splunk, ELK |
| Code Agent | Source code | GitHub, GitLab, code analysis |
| Infrastructure Agent | Cloud resources | AWS, GCP, Azure, Terraform |
| Database Agent | Data systems | PostgreSQL, MySQL, MongoDB |
| Security Agent | Security events | SIEM, vulnerability scanners |
| Network Agent | Connectivity | DNS, load balancers, CDN |
| Performance Agent | Metrics/APM | New Relic, Dynatrace |
| Deployment Agent | CI/CD | Jenkins, ArgoCD, Kubernetes |
| Communication Agent | Customer comms | Slack, email, status pages |
| Documentation Agent | Knowledge base | Confluence, Notion, wikis |

---

### Swarm Coordinator

**Definition:** A meta-agent that orchestrates multiple specialist agents and synthesizes their findings.

**Responsibilities:**
- Dispatch tasks to appropriate agents
- Track parallel investigation progress
- Synthesize findings from multiple agents
- Resolve conflicts between agent conclusions
- Determine when consensus is reached

---

### Meta-Orchestrator

**Definition:** The top-level system component that selects execution mode and assigns agents based on ticket complexity.

**Decision Factors:**
- Ticket content analysis
- Severity level
- Customer tier
- Historical patterns
- Current system load

---

## Confidence & Governance

### Confidence Score

**Definition:** A 0-100% measure of how certain the AI is about its conclusion.

**Calculation Based On:**
- Evidence strength supporting hypothesis
- Evidence against hypothesis
- Number of corroborating sources
- Historical accuracy on similar issues

**Governance Thresholds:**
| Confidence | Action | Human Involvement |
|------------|--------|-------------------|
| ≥95% | Auto-execute | None (logged) |
| 85-94% | Execute + review | Post-action review |
| 70-84% | Await approval | Pre-action approval |
| <70% | Escalate | Human takes over |

---

### Autonomy Level

**Definition:** The degree of independent action an agent can take without human approval.

**Spectrum:**
```
Full Human Control ◄─────────────────────────────► Full Autonomy
        │                    │                         │
   Human-Led            Supervised              Auto-Execute
      Mode               Autonomy                  Mode
```

---

### Human-in-the-Loop (HITL)

**Definition:** Design pattern where human judgment is integrated into automated workflows at critical decision points.

**HACI Implementation:**
- Approval gates before high-risk actions
- Review queues for medium-confidence findings
- Escalation paths when AI is uncertain
- Override capabilities at any point

---

### Approval Gate

**Definition:** A checkpoint where workflow pauses for human review and approval.

**Trigger Conditions:**
- Confidence below threshold
- High-severity ticket
- Enterprise customer
- Destructive action proposed
- Policy requirement

---

### Escalation

**Definition:** Transferring an investigation from AI to human operator when AI cannot resolve confidently.

**Escalation Triggers:**
- Max iterations reached without resolution
- Confidence remains below threshold
- Conflicting evidence
- Novel/unprecedented situation
- Customer request

---

## Architecture Components

### Context Bus

**Definition:** The shared memory system that allows agents to share information during investigations.

**Implementation:** Redis-based pub/sub + state store

**Contains:**
- Current investigation state
- Shared observations
- Agent findings
- Coordination messages

---

### System of Record (SoR)

**Definition:** The persistent database storing all investigation history, decisions, and audit trails.

**Implementation:** PostgreSQL + TimescaleDB

**Stores:**
- Complete investigation timelines
- All agent decisions with reasoning
- Tool call logs
- Human approvals
- Performance metrics

---

### Checkpointer

**Definition:** Component that saves graph state at each node, enabling pause/resume and recovery.

**Purpose:**
- Resume interrupted investigations
- Recover from failures
- Support human-in-the-loop pauses
- Enable time-travel debugging

---

### State Graph

**Definition:** LangGraph's representation of the workflow as nodes (functions) and edges (transitions).

**HACI Graphs:**
- **Harness Graph:** THINK→ACT→OBSERVE→EVALUATE loop
- **Swarm Graph:** Parallel agent dispatch + synthesis
- **Approval Graph:** Human review workflow

---

## Context Engineering

### Context Layer

**Definition:** A category of information injected into agent prompts, organized by type and priority.

**HACI Layers:**
| Layer | Content | Token Budget |
|-------|---------|--------------|
| L1: Foundational | System prompt, agent identity, capabilities | ~5K |
| L2: Situational | Ticket details, customer context | ~10K |
| L3: Operational | Current investigation state, findings | ~15K |
| L4: Dynamic | Retrieved knowledge, RAG results | ~20K |

---

### Token Budget

**Definition:** The allocated number of tokens for each context layer to stay within LLM limits.

**Purpose:** Ensure critical information fits within context window while maximizing relevant content.

---

### RAG (Retrieval-Augmented Generation)

**Definition:** Technique that retrieves relevant documents and includes them in the prompt to ground AI responses in specific knowledge.

**HACI Usage:** Pull relevant runbooks, past incidents, and documentation into agent context.

---

## Integration Concepts

### MCP (Model Context Protocol)

**Definition:** Anthropic's open standard for connecting AI models to external tools and data sources.

**Benefits:**
- Standardized tool interface
- Credential isolation
- Pre-built integrations
- Reduced development time

---

### Tool Binding

**Definition:** The process of making external tools available to an LLM so it can invoke them.

**Example:** Binding the `search_logs` tool allows the agent to query Datadog by calling the tool with parameters.

---

### Vendor Integration

**Definition:** Connection between HACI and external systems (monitoring, ticketing, cloud providers, etc.).

**Integration Methods:**
| Method | Use Case |
|--------|----------|
| MCP Server | Standardized, credential-isolated |
| Direct API | Performance-critical, custom logic |
| Webhook | Event-driven, real-time |
| Polling | Legacy systems, no webhook support |

---

## Observability Terms

### Trace

**Definition:** A complete record of an operation's execution path, including all nested calls.

**HACI Traces Include:**
- LLM invocations with prompts/responses
- Tool calls with inputs/outputs
- State transitions
- Timing information
- Token usage

---

### Span

**Definition:** A single unit of work within a trace (e.g., one LLM call, one tool execution).

---

### Run

**Definition:** In LangSmith, a single execution of a chain, agent, or tool. Runs can be nested.

---

### Evaluation Dataset

**Definition:** A curated set of inputs and expected outputs used to measure AI performance.

**Example:** 100 historical tickets with known root causes used to test HACI accuracy.

---

## Performance Metrics

### MTTR (Mean Time to Resolution)

**Definition:** Average time from ticket creation to resolution.

**HACI Target:** <30 minutes (vs. 4+ hours manual)

---

### Auto-Resolution Rate

**Definition:** Percentage of tickets resolved by AI without human intervention.

**HACI Target:** 85%

---

### Confidence Calibration

**Definition:** How well AI confidence scores predict actual accuracy.

**Ideal:** 80% confidence should be correct ~80% of the time.

---

### First-Contact Resolution

**Definition:** Percentage of tickets resolved without escalation or reassignment.

**HACI Target:** 90%

---

## Governance Terms

### Audit Trail

**Definition:** Complete, immutable record of all actions and decisions for compliance and review.

---

### Risk Level

**Definition:** Classification of proposed action based on potential impact.

| Risk Level | Examples |
|------------|----------|
| Low | Read-only queries, status checks |
| Medium | Configuration changes, restarts |
| High | Data modifications, deployments |
| Critical | Security changes, data deletion |

---

### Governance Framework

**Definition:** The policies, procedures, and controls that ensure AI operates safely and compliantly.

**HACI Framework Pillars:**
1. Ethical AI Principles
2. Human Oversight
3. Security & Privacy
4. Compliance Management
5. Continuous Improvement

---

## Common Acronyms

| Acronym | Full Form |
|---------|-----------|
| HACI | Harness-Enhanced Agentic Collaborative Intelligence |
| HITL | Human-in-the-Loop |
| MCP | Model Context Protocol |
| RAG | Retrieval-Augmented Generation |
| LLM | Large Language Model |
| MTTR | Mean Time to Resolution |
| SoR | System of Record |
| API | Application Programming Interface |
| CI/CD | Continuous Integration / Continuous Deployment |
| SLA | Service Level Agreement |
| RBAC | Role-Based Access Control |
| PII | Personally Identifiable Information |

---

## Related Concepts (External)

### LangGraph

**Definition:** LangChain's framework for building stateful, multi-actor applications with LLMs as graphs.

**HACI Usage:** Core execution engine for harness and swarm graphs.

---

### LangSmith

**Definition:** LangChain's platform for LLM application observability, testing, and evaluation.

**HACI Usage:** Tracing, monitoring, evaluation datasets, prompt management.

---

### LangChain

**Definition:** Framework for developing applications powered by language models.

**HACI Usage:** Tool abstractions, prompt templates, LLM integrations.

---

## See Also

- [Quick Start Guide](./HACI_Quick_Start_Guide.md) - Get running in 15 minutes
- [FAQ](./HACI_FAQ.md) - Common questions answered
- [Technical Documentation](./HACI_Comprehensive_Technical_Documentation.md) - Deep architectural details
- [Implementation Guide](./HACI_LangSmith_Implementation_Guide.md) - Full build instructions
