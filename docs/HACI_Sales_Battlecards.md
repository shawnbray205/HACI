# HACI Sales Battlecards

> Competitive positioning, objection handling, and sales enablement guide

---

## Quick Reference

### HACI Elevator Pitch (30 seconds)

> "HACI is an AI-powered operations platform that automatically investigates and resolves support tickets. Unlike basic chatbots or rigid runbooks, HACI uses a structured reasoning framework with multiple specialist AI agents that work together—like having a team of expert engineers available 24/7. The result: 90% faster resolution times, 85% of issues resolved without human intervention, and your engineers freed up to build instead of firefight."

### Key Differentiators (Memorize These)

| # | Differentiator | Why It Matters |
|---|----------------|----------------|
| 1 | **Structured Harness** | Predictable, auditable AI (not a black box) |
| 2 | **Multi-Agent Swarms** | Parallel investigation = faster + more thorough |
| 3 | **Calibrated Autonomy** | Right level of human oversight for each situation |
| 4 | **Multi-LLM Architecture** | Best model for each task, 90% cost savings |
| 5 | **Enterprise Governance** | Built for compliance, not bolted on |

### Ideal Customer Profile

**Best Fit:**
- 500+ support tickets/month
- Complex technical environment (multiple tools, services)
- 24/7 availability requirements
- DevOps/SRE team feeling overwhelmed
- Budget for automation ($50K+/year)

**Warning Signs (Potential Bad Fit):**
- Very small volume (<100 tickets/month)
- Single, simple application
- No existing monitoring/observability
- "Just want a chatbot"
- Extremely price-sensitive (<$20K budget)

---

## Competitive Battlecards

### vs. Traditional Runbook Automation

**Competitor Examples:** Rundeck, StackStorm, Ansible Tower, custom scripts

**Positioning:** "Runbooks are great for known, repetitive issues. But what about the other 40%?"

| Capability | Runbooks | HACI |
|------------|----------|------|
| Known issues | ✅ Great | ✅ Great |
| Novel issues | ❌ Fails silently | ✅ Reasons through |
| Partial matches | ❌ Exact match only | ✅ Semantic understanding |
| Multi-step reasoning | ❌ Pre-scripted only | ✅ Dynamic investigation |
| Learning | ❌ Manual updates | ✅ Improves from feedback |
| Maintenance | High (per runbook) | Low (model updates) |

**Key Questions to Ask:**
- "What percentage of your incidents don't match existing runbooks?"
- "How much time do you spend maintaining and updating runbooks?"
- "What happens when an issue is similar but not exactly matching a runbook?"

**Winning Statement:**
> "HACI doesn't replace your runbooks—it uses them. But when an issue doesn't match, HACI reasons through it like an expert engineer would, using your tools and context. You get the best of both worlds."

---

### vs. Single AI Agent Solutions

**Competitor Examples:** Generic LLM wrappers, simple AI assistants, ChatGPT plugins

**Positioning:** "A single generalist AI can't match the depth of specialized experts working together."

| Capability | Single Agent | HACI Multi-Agent |
|------------|--------------|------------------|
| Simple issues | ✅ Handles well | ✅ Handles well |
| Complex issues | ⚠️ Sequential, slow | ✅ Parallel, fast |
| Domain expertise | ⚠️ Jack of all trades | ✅ Specialists per domain |
| Context limits | ❌ Hits token limits | ✅ Distributed context |
| Single point of failure | ❌ Yes | ✅ Graceful degradation |
| Accuracy on complex | ⚠️ Lower | ✅ Higher (consensus) |

**Key Questions to Ask:**
- "How do you handle issues that span multiple systems—logs, code, infrastructure, database?"
- "What's your current MTTR on complex, multi-system incidents?"
- "Have you tried AI assistants but found they give generic or wrong answers?"

**Winning Statement:**
> "When you have a complex incident, you don't send one junior engineer—you bring together your log expert, your database expert, your infrastructure expert. HACI does the same thing with AI: specialist agents working in parallel, then synthesizing their findings."

---

### vs. Vendor-Specific AI (Datadog AI, PagerDuty AI, etc.)

**Competitor Examples:** Datadog Bits AI, PagerDuty AIOps, New Relic NRQL AI

**Positioning:** "Vendor AI only sees their piece of the puzzle. HACI sees the whole picture."

| Capability | Vendor AI | HACI |
|------------|-----------|------|
| Their platform | ✅ Deep | ✅ Integrated |
| Other tools | ❌ Limited/none | ✅ 50+ integrations |
| Cross-platform correlation | ❌ No | ✅ Yes |
| Action capabilities | ⚠️ Limited to their platform | ✅ Execute anywhere |
| Vendor independence | ❌ Locked in | ✅ Works with any stack |
| Custom integrations | ⚠️ Limited | ✅ Extensible |

**Key Questions to Ask:**
- "How many different monitoring and infrastructure tools do you use?"
- "When you have an incident, do you have to check multiple dashboards?"
- "Has vendor-specific AI ever missed the root cause because it couldn't see another system?"

**Winning Statement:**
> "Datadog AI is excellent at finding issues in Datadog. But your incidents don't live in one tool—they span logs, metrics, traces, code, infrastructure, databases. HACI correlates across all of them."

---

### vs. ServiceNow Virtual Agent / ITSM AI

**Competitor Examples:** ServiceNow Virtual Agent, BMC Helix, Freshservice Freddy

**Positioning:** "ITSM AI is for service desk tickets. HACI is for technical investigation."

| Capability | ITSM AI | HACI |
|------------|---------|------|
| Password resets | ✅ Great | ⚠️ Overkill |
| IT service requests | ✅ Great | ⚠️ Not focus |
| Technical investigation | ❌ Shallow | ✅ Deep |
| Root cause analysis | ❌ Limited | ✅ Comprehensive |
| Tool integration | ⚠️ ITSM-centric | ✅ DevOps/SRE tools |
| Developer/SRE focus | ❌ IT focus | ✅ Built for |

**Key Questions to Ask:**
- "Are your biggest pain points service desk tickets or technical incidents?"
- "Do you need AI that can actually log into your monitoring tools and investigate?"
- "Is your goal to deflect tickets or to actually resolve technical issues?"

**Winning Statement:**
> "ServiceNow is great for 'I need a new laptop.' HACI is for 'The API is returning 500 errors and customers can't check out.' Different problems, different solutions."

---

### vs. Building In-House

**Competitor:** Internal engineering team building custom AI ops tooling

**Positioning:** "You could build it—but should you?"

| Factor | Build In-House | Buy HACI |
|--------|----------------|----------|
| Time to value | 6-18 months | 4-8 weeks |
| Engineering cost | $500K-$2M | Subscription |
| Ongoing maintenance | Your team | Our team |
| LLM optimization | You figure it out | Battle-tested |
| Multi-agent coordination | Complex | Included |
| Updates/improvements | Your roadmap | Continuous |
| Risk | High (new territory) | Low (proven) |

**Key Questions to Ask:**
- "How long would it take your team to build this? What else wouldn't they be building?"
- "Do you have LLM operations expertise in-house?"
- "What's your core business—building AI ops tools or building your product?"

**Winning Statement:**
> "You absolutely could build this—your team is talented. The question is: should they? That's 6-12 months of your best engineers not working on your core product. And then you own maintaining it forever. Most companies find it's better to buy the solved problem and focus engineering on what makes them unique."

**Cost Comparison:**
```
Build In-House:
  Senior engineers (2 FTE x 12 months):     $600,000
  Infrastructure/LLM costs during dev:      $50,000
  Ongoing maintenance (1 FTE):              $200,000/year
  Opportunity cost:                         Priceless
  Total Year 1:                             $850,000+

Buy HACI:
  Annual subscription:                      $60,000-$150,000
  Implementation:                           $20,000-$50,000
  Total Year 1:                             $80,000-$200,000
```

---

## Objection Handling

### "It's too expensive"

**Response Framework:** Reframe to value, not cost

> "I understand budget is important. Let's look at what you're spending now. With 500 tickets/month and a 4-hour average MTTR, at $75/hour engineer cost, you're spending $150,000/year on incident response alone. HACI typically reduces that by 85%. The question isn't whether you can afford HACI—it's whether you can afford not to have it."

**Follow-up Questions:**
- "What's your current cost per incident?"
- "How much engineering time goes to incident response vs. feature work?"
- "What would an 85% reduction in incident response time be worth?"

---

### "We're worried about AI making mistakes"

**Response Framework:** Acknowledge, then explain safeguards

> "That's exactly the right concern—and it's why we built HACI differently. Three key safeguards: First, the harness pattern means every action is deliberate and traceable, not a black box. Second, confidence-based autonomy means HACI only acts independently when it's highly certain. Third, human approval gates ensure a person reviews anything risky. You can see every step HACI took and why."

**Key Points:**
- 95%+ confidence required for auto-resolution (configurable)
- Human approval required for destructive actions
- Full audit trail of all decisions
- Easy override at any point
- Accuracy improves with feedback

---

### "What if AI hallucinates or gives wrong answers?"

**Response Framework:** Differentiate HACI's approach

> "Great question. Unlike ChatGPT responding to random questions, HACI is grounded in your actual data. It's not making things up—it's querying your real logs, metrics, and infrastructure. The harness pattern forces evidence-based reasoning: form hypothesis, gather evidence, evaluate. And the confidence scoring means HACI won't claim certainty it doesn't have. When confidence is low, it escalates to humans."

**Key Points:**
- Evidence-based, not knowledge-based
- Queries actual systems, doesn't rely on training data
- Confidence calibration prevents overconfidence
- Low confidence = human involvement
- Continuous accuracy monitoring

---

### "Our environment is too complex/unique"

**Response Framework:** Complexity is HACI's strength

> "Complex environments are actually where HACI shines most. That's exactly why we built multi-agent swarms—to handle the complexity that single-agent solutions can't. The more tools and systems you have, the more valuable HACI's ability to correlate across them becomes. We'd love to do a technical deep-dive on your architecture."

**Follow-up:**
- "Walk me through your most complex recent incident"
- "How many different systems did you have to check?"
- "What would parallel investigation across all those systems be worth?"

---

### "We don't trust AI with production systems"

**Response Framework:** Start small, build trust

> "I completely respect that—trust has to be earned. That's why we recommend a phased approach. Start with HACI in read-only mode: it investigates and recommends, but every action requires your approval. You watch it work, see its reasoning, correct it when needed. Only when you're comfortable do we gradually increase autonomy. Most customers take 4-8 weeks to reach full confidence."

**Trust-Building Path:**
1. Week 1-2: Read-only, recommendations only
2. Week 3-4: Low-risk auto-actions (queries, notifications)
3. Week 5-6: Medium-risk with approval
4. Week 7-8: High-confidence auto-resolution
5. Ongoing: Calibrate based on results

---

### "We already have good runbooks/automation"

**Response Framework:** Complement, don't replace

> "That's great—and those runbooks are valuable. HACI actually uses your existing runbooks as part of its knowledge base. The question is: what percentage of incidents match your runbooks exactly? For most teams, it's 50-60%. HACI handles the other 40% that don't match—the novel issues, the edge cases, the variations. Plus, HACI can automatically create runbooks from successful investigations."

---

### "Our team likes handling incidents themselves"

**Response Framework:** Free them for interesting work

> "I hear that—a lot of engineers take pride in their incident response skills. But is that really how they want to spend their time? When we talk to engineers after HACI deployment, the common feedback is: 'I still handle the interesting, complex incidents. But I don't miss the 3 AM pages for routine issues.' HACI handles the repetitive stuff so your team can focus on the challenging work they actually enjoy."

---

### "What about security/compliance?"

**Response Framework:** Built-in, not bolted-on

> "Security and compliance are core to HACI's architecture, not afterthoughts. We're SOC 2 Type II designed, with complete audit trails, role-based access control, and encryption throughout. For regulated industries, we support HIPAA, SOX, and GDPR requirements including PII detection and data minimization. Happy to do a security review with your team."

**Security Highlights:**
- No credentials stored (secret manager integration)
- Complete audit trail (every action logged)
- Configurable data retention
- PII detection and redaction
- Encryption at rest and in transit
- RBAC aligned with your IAM

---

### "We need to talk to other customers"

**Response Framework:** Happy to facilitate

> "Absolutely—reference calls are valuable. We can connect you with customers in your industry and of similar size. We also have case studies available. What specific questions would you want answered?"

**Have Ready:**
- 2-3 reference customers in their vertical
- Relevant case studies
- Third-party reviews/analyst reports

---

### "Let us think about it"

**Response Framework:** Create urgency with value

> "Of course—this is an important decision. While you're evaluating, let me share one data point: most customers find that every month of delay costs them $X in incident response time that could be automated. Would it make sense to start with a focused POC on your highest-pain-point area? That way you can make the decision based on real results in your environment."

**Next Step Options:**
- Technical deep-dive call
- POC scoping session
- ROI analysis with their numbers
- Reference call with similar customer

---

## Discovery Questions

### Pain Discovery

1. "Walk me through what happens when an alert fires at 3 AM"
2. "How much of your engineering time goes to incident response vs. feature work?"
3. "What was your most painful incident in the last quarter?"
4. "How long does a typical incident take to resolve?"
5. "What's your current on-call rotation look like?"

### Environment Discovery

6. "What monitoring and observability tools are you using?"
7. "Walk me through your typical incident investigation workflow"
8. "How many different systems might be involved in a complex incident?"
9. "What's your ticketing/incident management system?"
10. "Are there any compliance requirements we should know about?"

### Decision Process Discovery

11. "Who else would be involved in a decision like this?"
12. "What does your evaluation process typically look like?"
13. "Have you looked at other solutions in this space?"
14. "What would make this a successful project from your perspective?"
15. "What's your timeline for making a decision?"

### Budget Discovery

16. "Is there budget allocated for DevOps/SRE tooling this year?"
17. "How do you typically evaluate ROI for automation investments?"
18. "What would the approval process look like for an investment of this size?"

---

## Demo Script Outline

### Opening (2 minutes)

"Let me show you how HACI would handle an incident in your environment. I'll use a scenario similar to what you described—[reference their pain point]."

### Ticket Intake (2 minutes)

"Here's a ticket coming in from PagerDuty. Notice how HACI immediately starts analyzing, not waiting for human triage."

**Show:** Ticket appearing, meta-orchestrator selecting mode

### Investigation (5 minutes)

"Watch the harness in action. THINK: it's forming hypotheses. ACT: it's querying your tools—Datadog, AWS, your database. OBSERVE: analyzing results."

**Show:** Timeline building, tools being called, evidence accumulating

### Multi-Agent (3 minutes)

"Now it's getting interesting. HACI recognized this needs multiple perspectives, so it's spinning up a micro-swarm. Log Agent, Infrastructure Agent, and Database Agent working in parallel."

**Show:** Swarm coordination, parallel investigation

### Finding & Approval (3 minutes)

"HACI has reached 87% confidence—below the auto-resolve threshold, so it's asking for approval. Here's its finding, here's the evidence, here's the proposed action."

**Show:** Approval interface, evidence summary

### Resolution (2 minutes)

"I'll approve this. HACI executes the fix... and confirms resolution. Total time: 8 minutes. What would this have taken manually?"

### Audit Trail (2 minutes)

"For compliance, here's the complete audit trail. Every decision, every tool call, every piece of reasoning. This goes to your SIEM or wherever you need it."

**Show:** Audit log, compliance report

### Q&A (5+ minutes)

"What questions do you have? What would you want to see in a POC?"

---

## Pricing Guidance

### Factors That Increase Price

- Higher ticket volume
- More integrations
- Enterprise compliance requirements
- On-premises deployment
- Custom development
- Premium support SLA

### Factors That Decrease Price

- Annual commitment (vs. monthly)
- Multi-year deal
- Design partner/case study participation
- Lower support tier

### Typical Deal Sizes

| Segment | Annual Range | Notes |
|---------|--------------|-------|
| SMB | $30K-$60K | Standard features, cloud deployment |
| Mid-Market | $60K-$150K | More integrations, enhanced support |
| Enterprise | $150K-$500K | Full platform, compliance, custom |
| Strategic | $500K+ | Multi-region, dedicated resources |

### ROI Talking Points

- "For every $1 spent on HACI, customers typically save $5-10"
- "Average payback period is 2-4 months"
- "The platform often pays for itself in reduced after-hours costs alone"

---

## Competitive Intelligence Sources

**Stay Updated On:**
- Datadog Bits AI announcements
- PagerDuty AIOps features
- ServiceNow Virtual Agent updates
- New entrants in AI ops space

**Resources:**
- G2 Crowd reviews (ours and competitors)
- Gartner AIOps Market Guide
- Forrester analyst reports
- Competitor pricing pages and feature lists

---

## Quick Wins for New Reps

1. **Learn the harness** - Be able to explain THINK→ACT→OBSERVE→EVALUATE simply
2. **Memorize 3 case studies** - One for your target vertical
3. **Know the ROI math** - Be able to do napkin ROI on the spot
4. **Practice objection responses** - Top 5 objections, smooth responses
5. **Demo confidently** - Nothing kills a deal like a fumbled demo

---

*Confidential - Internal Sales Use Only*

*Last updated: January 2026 | Version 1.0*
