# HACI Frequently Asked Questions

> Answers to the most common questions about Harness-Enhanced Agentic Collaborative Intelligence

---

## Table of Contents

1. [General Questions](#general-questions)
2. [Technical Architecture](#technical-architecture)
3. [Security & Compliance](#security--compliance)
4. [Integration & Compatibility](#integration--compatibility)
5. [Pricing & ROI](#pricing--roi)
6. [Implementation & Deployment](#implementation--deployment)
7. [Comparison Questions](#comparison-questions)
8. [Operations & Support](#operations--support)

---

## General Questions

### What is HACI?

**HACI (Harness-Enhanced Agentic Collaborative Intelligence)** is an AI-powered automation platform for enterprise support and DevOps operations. It combines:

- **Structured reasoning** via the THINK→ACT→OBSERVE→EVALUATE harness
- **Multi-agent collaboration** for complex problem-solving
- **Calibrated human oversight** based on confidence levels
- **Enterprise integrations** with 50+ monitoring, ticketing, and infrastructure tools

HACI automatically investigates support tickets, identifies root causes, and resolves issues—escalating to humans only when necessary.

---

### How is HACI different from ChatGPT or Claude?

| Aspect | ChatGPT/Claude | HACI |
|--------|----------------|------|
| **Purpose** | General conversation | Specialized support automation |
| **Structure** | Free-form responses | Structured harness (THINK→ACT→OBSERVE→EVALUATE) |
| **Tools** | Limited/none | 50+ enterprise integrations |
| **Memory** | Session-based | Persistent investigation state |
| **Autonomy** | User-driven | Confidence-calibrated autonomy |
| **Multi-agent** | Single model | Coordinated specialist agents |
| **Audit trail** | Chat logs | Complete decision audit |

**Bottom line:** ChatGPT is a conversational AI. HACI is an autonomous operations platform with built-in governance.

---

### What problems does HACI solve?

1. **Alert fatigue:** Automatically triages and resolves routine issues
2. **Slow incident response:** Reduces MTTR from 4+ hours to <30 minutes
3. **Knowledge silos:** AI captures and applies tribal knowledge consistently
4. **Scaling limitations:** Handles volume spikes without proportional staff increases
5. **After-hours coverage:** 24/7 automated response without overnight staffing
6. **Inconsistent resolution:** Standardized investigation methodology every time

---

### Who is HACI for?

**Primary Users:**
- DevOps/SRE teams managing complex infrastructure
- Support organizations handling technical tickets
- Platform teams enabling developer self-service
- Enterprises requiring compliance and audit trails

**Best Fit:**
- 500+ tickets/month
- Multiple monitoring/infrastructure tools
- 24/7 coverage requirements
- Need for consistent, auditable responses

---

### What's the "harness" in HACI?

The **harness** is HACI's core control pattern that structures how AI agents reason and act:

```
🧠 THINK    → Analyze input, form hypotheses
⚡ ACT      → Execute tools, gather evidence  
👁️ OBSERVE  → Interpret results, extract insights
✅ EVALUATE → Decide: continue, complete, or escalate
```

This loop continues until the agent reaches sufficient confidence or a human takes over.

**Why it matters:** The harness prevents AI from "going off the rails"—every action is deliberate, traceable, and bounded.

---

### What's the "swarm" in HACI?

For complex issues, HACI deploys **multiple specialist agents in parallel**:

- Log Agent analyzes error logs
- Infrastructure Agent checks cloud resources
- Database Agent examines query performance
- Code Agent reviews recent changes
- ...all simultaneously

A **Swarm Coordinator** synthesizes their findings into a unified conclusion.

**Result:** Faster resolution through parallelism + more thorough analysis through specialization.

---

## Technical Architecture

### What LLMs does HACI use?

HACI is **multi-provider by design**, optimizing cost and capability:

| Provider | Models | Use Case | % of Calls |
|----------|--------|----------|------------|
| Google | Gemini Flash | Simple queries, fast triage | ~55% |
| Anthropic | Claude Sonnet | Code analysis, balanced tasks | ~30% |
| Anthropic | Claude Opus | Complex orchestration | ~10% |
| OpenAI | GPT-4o | Multi-modal, conversation | ~4% |
| OpenAI | o1 | Deep reasoning | ~1% |

**This approach reduces costs by ~90%** compared to using a single premium model for everything.

---

### Can HACI work with just one LLM provider?

Yes. While multi-provider is optimal, HACI works with any single provider:

- **Anthropic-only:** Claude Haiku → Sonnet → Opus routing
- **OpenAI-only:** GPT-4o-mini → GPT-4o → o1 routing
- **Google-only:** Gemini Flash → Pro → Ultra routing

Contact us for provider-specific configuration guidance.

---

### What infrastructure does HACI require?

**Minimum (Development/POC):**
- Docker or Kubernetes cluster
- PostgreSQL database
- Redis instance
- LLM API access

**Production Recommended:**
- Kubernetes (3+ nodes)
- PostgreSQL (with HA/replication)
- Redis Cluster
- LangSmith account (observability)
- Object storage (artifacts)

**Cloud Options:**
- AWS EKS + RDS + ElastiCache
- GCP GKE + Cloud SQL + Memorystore
- Azure AKS + PostgreSQL + Redis Cache

---

### How does HACI maintain state across the harness loop?

HACI uses **LangGraph checkpointing** with PostgreSQL:

- Every node transition saves complete state
- Investigations can pause/resume at any point
- Human-in-the-loop approvals don't lose context
- System failures recover from last checkpoint
- Full state history for audit and debugging

---

### What's the latency for a typical investigation?

| Ticket Complexity | Typical Duration | Iterations |
|-------------------|------------------|------------|
| Simple | 2-5 minutes | 1-2 |
| Moderate | 5-15 minutes | 2-4 |
| Complex | 15-45 minutes | 4-8 |
| Multi-agent swarm | 10-30 minutes | 2-4 per agent |

**Note:** Swarm investigations are faster than sequential because agents work in parallel.

---

### How does HACI handle tool failures?

**Graceful degradation:**

1. **Retry with backoff** for transient failures
2. **Alternative tools** when available (e.g., different log source)
3. **Partial results** - continue with available data
4. **Escalation** if critical tools unavailable

**Example:** If Datadog is unreachable, HACI notes this gap, continues with other tools, and may escalate if log analysis was critical.

---

## Security & Compliance

### Is HACI SOC 2 compliant?

HACI is designed for **SOC 2 Type II readiness**:

- Complete audit trails for all actions
- Role-based access control (RBAC)
- Encryption at rest and in transit
- Credential isolation via secret management
- Automated compliance reporting

**Note:** Actual certification depends on deployment environment and customer controls.

---

### How are credentials handled?

HACI **never stores credentials directly**:

- API keys → External secret managers (Vault, AWS Secrets Manager)
- OAuth tokens → Delegated authentication
- MCP integrations → Credential isolation at server level
- No credentials in logs or traces

---

### Can HACI access production data?

**Configurable by policy:**

| Access Level | What HACI Can Do |
|--------------|------------------|
| Read-Only | Query logs, metrics, configs |
| Limited Write | Create tickets, post comments |
| Managed Write | Restart services, scale resources |
| Full | All operations (rare, requires approval) |

Most deployments use **read-only + limited write** with approval gates for any changes.

---

### How is PII handled?

- **Detection:** Automatic PII detection in logs and tickets
- **Redaction:** Configurable redaction before LLM processing
- **Minimization:** Only necessary context sent to LLMs
- **Audit:** All data access logged
- **Retention:** Configurable retention policies

---

### Is HACI GDPR/HIPAA compatible?

HACI provides features for compliance, but **compliance depends on deployment**:

**GDPR:**
- Data minimization controls
- Right to deletion support
- Processing records
- EU data residency options

**HIPAA:**
- Audit logging
- Access controls
- PHI detection/redaction
- BAA support with LLM providers (where available)

**Recommendation:** Engage compliance team during implementation.

---

## Integration & Compatibility

### What tools does HACI integrate with?

**50+ integrations across categories:**

| Category | Examples |
|----------|----------|
| **Monitoring** | Datadog, New Relic, Dynatrace, Prometheus |
| **Logging** | Splunk, ELK, Sumo Logic, CloudWatch Logs |
| **Ticketing** | Jira, ServiceNow, Zendesk, PagerDuty |
| **Cloud** | AWS, GCP, Azure, Kubernetes |
| **Code** | GitHub, GitLab, Bitbucket |
| **Communication** | Slack, Teams, email |
| **Databases** | PostgreSQL, MySQL, MongoDB, Redis |

See the [Vendor Integration Matrix](./HACI_Vendor_Integration_Matrix.md) for complete details.

---

### How long does integration take?

| Integration Type | Time | Effort |
|------------------|------|--------|
| Pre-built MCP | 1-2 hours | Configuration only |
| Pre-built API | 2-4 hours | API key + config |
| Custom webhook | 1-2 days | Light development |
| Custom API | 3-5 days | Moderate development |

**Most common integrations (Datadog, Jira, Slack, AWS) take under 4 hours.**

---

### Can HACI work with our custom/internal tools?

Yes, via multiple methods:

1. **Custom MCP Server:** Build a server exposing your tool's API
2. **Direct API Integration:** Add custom tool to agent's toolkit
3. **Webhook Interface:** HACI calls your tool via HTTP
4. **Script Execution:** Run custom scripts with sandboxed execution

We provide templates and guidance for custom integrations.

---

### Does HACI replace our existing tools?

**No.** HACI **orchestrates and enhances** existing tools:

- Queries your existing monitoring (Datadog, etc.)
- Creates tickets in your existing system (Jira, etc.)
- Communicates via your existing channels (Slack, etc.)
- Deploys through your existing CI/CD (Jenkins, etc.)

HACI adds intelligence, not infrastructure.

---

## Pricing & ROI

### How is HACI priced?

**Contact us for detailed pricing.** Models include:

- **Per-ticket:** Based on investigation volume
- **Per-seat:** Based on operator licenses
- **Platform fee:** Fixed + usage-based hybrid
- **Enterprise:** Custom agreements

**Factors affecting price:**
- Monthly ticket volume
- Number of integrations
- Support tier (standard/premium/enterprise)
- Deployment model (cloud/on-prem)

---

### What's the typical ROI?

**Based on customer deployments:**

| Metric | Before HACI | After HACI | Improvement |
|--------|-------------|------------|-------------|
| MTTR | 4+ hours | 22 minutes | 91% faster |
| Cost/ticket | $57.50 | $1.54 | 97% reduction |
| Auto-resolution | 0% | 85% | New capability |
| After-hours staffing | 2-4 FTE | 0.5 FTE | 75% reduction |

**Typical payback period:** 2-4 months

**5-year ROI:** 500-800%

---

### What are the LLM costs?

**Typical LLM cost per ticket:** $0.08 - $0.25

| Ticket Type | Avg Tokens | Avg LLM Cost |
|-------------|------------|--------------|
| Simple (single agent) | ~8K | $0.08 |
| Moderate (2-3 iterations) | ~20K | $0.15 |
| Complex (swarm) | ~50K | $0.25 |

**Cost optimization via multi-provider routing saves ~90%** vs. using premium models for everything.

---

### Hidden costs to consider?

**Transparent about total cost:**

| Cost Category | Typical Range |
|---------------|---------------|
| HACI license | Varies by plan |
| LLM API usage | $0.10/ticket avg |
| Infrastructure | $500-2000/month |
| Integration effort | 40-80 hours initial |
| Training | 8-16 hours |

**What's NOT charged:**
- Per-user fees for dashboard access
- Integration connector fees
- Basic support

---

## Implementation & Deployment

### How long does implementation take?

| Phase | Duration | Activities |
|-------|----------|------------|
| Discovery | 1-2 weeks | Requirements, architecture review |
| POC | 2-4 weeks | Limited deployment, validation |
| Pilot | 4-8 weeks | Production subset, tuning |
| Full rollout | 4-8 weeks | Organization-wide deployment |

**Total: 3-6 months** for enterprise deployment

**Accelerated option:** 4-8 weeks for teams with mature DevOps practices

---

### What does our team need to do?

**Customer responsibilities:**

1. **Access provisioning:** API keys for tools HACI will use
2. **Integration configuration:** Endpoint URLs, credentials
3. **Policy definition:** Autonomy levels, approval workflows
4. **Knowledge input:** Runbooks, escalation paths, team structure
5. **Testing participation:** Validate results during pilot
6. **Change management:** Team training and communication

**We handle:** Platform deployment, integration development, optimization

---

### Can we start with a pilot?

**Absolutely. Recommended pilot approach:**

1. **Scope:** Single team or ticket category
2. **Duration:** 4-8 weeks
3. **Volume:** 50-200 tickets
4. **Success criteria:** MTTR reduction, accuracy, user satisfaction

**Pilot deliverables:**
- Performance metrics vs. baseline
- Accuracy assessment
- User feedback summary
- Scaling recommendations

---

### Cloud vs. on-premises?

| Deployment | Best For | Considerations |
|------------|----------|----------------|
| **HACI Cloud** | Fastest deployment, managed operations | Data leaves your network |
| **Private Cloud** | Data residency, existing cloud investment | You manage infrastructure |
| **On-Premises** | Strict compliance, air-gapped environments | Most operational overhead |

**Most customers choose:** Private cloud (AWS/GCP/Azure) for balance of control and convenience.

---

## Comparison Questions

### Why not just use runbook automation?

| Capability | Runbooks | HACI |
|------------|----------|------|
| Novel issues | ❌ Fails | ✅ Reasons through |
| Pattern matching | Exact match only | Semantic understanding |
| Multi-step reasoning | Predefined only | Dynamic investigation |
| Learning | Manual updates | Continuous improvement |
| Maintenance | High (per runbook) | Low (model updates) |

**Runbooks:** Great for known, repetitive issues
**HACI:** Handles known AND unknown issues

---

### Why not just use a single AI agent?

| Capability | Single Agent | HACI Multi-Agent |
|------------|--------------|------------------|
| Complex issues | Sequential, slow | Parallel, fast |
| Specialization | Jack of all trades | Domain experts |
| Context limits | Hits token limits | Distributed context |
| Failure impact | Single point | Graceful degradation |
| Accuracy | Good | Better (consensus) |

**Single agent:** Fine for simple issues
**HACI:** Required for enterprise complexity

---

### How does HACI compare to PagerDuty/Datadog AI?

| Aspect | PagerDuty AI / Datadog AI | HACI |
|--------|---------------------------|------|
| **Scope** | Single vendor ecosystem | Multi-vendor orchestration |
| **Investigation depth** | Alert correlation | Full root cause analysis |
| **Tool access** | Own platform only | 50+ integrations |
| **Customization** | Limited | Fully configurable |
| **Human oversight** | Basic | Calibrated autonomy |
| **Multi-agent** | No | Yes |

**Vendor AI:** Good within their ecosystem
**HACI:** Orchestrates across your entire stack

---

### What about ServiceNow Virtual Agent?

| Aspect | ServiceNow VA | HACI |
|--------|---------------|------|
| **Focus** | IT service management | Technical investigation |
| **Investigation** | Guided flows | Autonomous reasoning |
| **Tool integration** | ServiceNow-centric | Tool-agnostic |
| **Deployment** | ServiceNow required | Independent platform |
| **LLM flexibility** | Limited | Multi-provider |

**ServiceNow VA:** Best for ServiceNow-heavy organizations
**HACI:** Best for heterogeneous tooling environments

---

## Operations & Support

### What happens when HACI is wrong?

**Confidence-based safeguards:**

1. **Low confidence → Human review** before action
2. **High-risk actions → Approval required** regardless of confidence
3. **Feedback loop:** Incorrect findings improve future accuracy
4. **Audit trail:** Full record of reasoning for review
5. **Override:** Humans can intervene at any point

**Wrong findings rate:** <5% for high-confidence conclusions

---

### How do we train HACI on our environment?

**HACI learns from:**

1. **Documentation:** Import runbooks, wikis, architecture docs
2. **Historical tickets:** Past incidents with resolutions
3. **Feedback:** Thumbs up/down on findings
4. **Corrections:** When humans override, HACI learns why
5. **Custom prompts:** Organization-specific guidance

**No ML training required**—HACI uses in-context learning and RAG.

---

### What support is included?

| Tier | Response Time | Channels | Included |
|------|---------------|----------|----------|
| **Standard** | 24 hours | Email, portal | Basic plans |
| **Premium** | 4 hours | + Slack, phone | Business plans |
| **Enterprise** | 1 hour | + Dedicated CSM | Enterprise plans |

**All tiers include:**
- Documentation access
- Community forum
- Quarterly reviews
- Version updates

---

### How do we measure HACI's performance?

**Built-in dashboards track:**

| Metric | Description |
|--------|-------------|
| Resolution rate | % tickets resolved without escalation |
| MTTR | Mean time to resolution |
| Accuracy | % findings confirmed correct |
| Confidence calibration | Confidence vs. actual accuracy |
| Cost per ticket | LLM + infrastructure costs |
| Human intervention rate | % requiring human involvement |

**Export options:** Prometheus metrics, Grafana dashboards, CSV reports

---

### What if we want to stop using HACI?

**No lock-in:**

- All investigation history exportable
- Standard data formats (JSON, CSV)
- No proprietary dependencies
- Integrations use standard protocols
- 30-day data retention after cancellation

**Exit assistance included** in enterprise plans.

---

## Still Have Questions?

- 📧 **Email:** sales@haci.ai
- 📅 **Schedule a demo:** calendly.com/haci-demo
- 💬 **Live chat:** Available on haci.ai
- 📖 **Documentation:** docs.haci.ai

---

## Related Resources

- [Quick Start Guide](./HACI_Quick_Start_Guide.md) - Get running in 15 minutes
- [Glossary](./HACI_Glossary.md) - All terminology explained
- [Technical Documentation](./HACI_Comprehensive_Technical_Documentation.md) - Architecture deep-dive
- [Comparison Matrices](./HACI_Comparison_Matrices.md) - Detailed competitive analysis
- [Executive Summary](./HACI_Executive_Summary.md) - Business case and ROI
