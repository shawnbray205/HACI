# HACI User Operations Manual

> The complete guide for support engineers and operators using HACI daily

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [Working with Investigations](#working-with-investigations)
4. [Approval Workflows](#approval-workflows)
5. [Monitoring & Alerts](#monitoring--alerts)
6. [Manual Interventions](#manual-interventions)
7. [Reporting & Analytics](#reporting--analytics)
8. [Best Practices](#best-practices)
9. [Keyboard Shortcuts](#keyboard-shortcuts)

---

## Getting Started

### Logging In

1. Navigate to your HACI instance: `https://haci.yourcompany.com`
2. Click **Sign in with SSO** (or enter credentials if using local auth)
3. Complete MFA if prompted
4. You'll land on the **Investigation Dashboard**

### First-Time Setup

On first login, configure your preferences:

1. Click your **profile icon** (top right) → **Settings**
2. Set your preferences:

| Setting | Recommended | Purpose |
|---------|-------------|---------|
| **Notification Channel** | Slack DM | Where you receive alerts |
| **Default View** | Active Investigations | Your landing page |
| **Time Zone** | Auto-detect | Timestamp display |
| **Sound Alerts** | On for Critical | Audio notification |
| **Email Digest** | Daily summary | End-of-day report |

3. Click **Save Preferences**

### Understanding Your Role

HACI has role-based permissions:

| Role | Can View | Can Approve | Can Configure | Can Admin |
|------|----------|-------------|---------------|-----------|
| **Viewer** | ✅ All investigations | ❌ | ❌ | ❌ |
| **Operator** | ✅ All investigations | ✅ Assigned | ❌ | ❌ |
| **Senior Operator** | ✅ All investigations | ✅ All | ✅ Policies | ❌ |
| **Admin** | ✅ All investigations | ✅ All | ✅ All | ✅ |

Your role appears in your profile menu. Contact your admin if you need elevated access.

---

## Dashboard Overview

### Main Navigation

```
┌─────────────────────────────────────────────────────────────────────────┐
│  🏠 HACI    [Investigations ▼]  [Approvals]  [Analytics]  [⚙️] [👤]    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  ACTIVE INVESTIGATIONS                              [+ New] [🔍] │   │
│  ├─────────────────────────────────────────────────────────────────┤   │
│  │  🔴 TICKET-4521  Database timeout errors         In Progress    │   │
│  │  🟡 TICKET-4519  API latency spike               Awaiting Approval│  │
│  │  🟢 TICKET-4518  Login failures resolved         Complete        │   │
│  │  ...                                                             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌──────────────────────┐  ┌──────────────────────┐                    │
│  │  PENDING APPROVALS   │  │  TODAY'S STATS       │                    │
│  │  3 awaiting action   │  │  47 resolved         │                    │
│  │  [View All →]        │  │  92% auto-resolved   │                    │
│  └──────────────────────┘  └──────────────────────┘                    │
└─────────────────────────────────────────────────────────────────────────┘
```

### Status Indicators

| Icon | Status | Meaning |
|------|--------|---------|
| 🔴 | **Critical** | High-severity, active investigation |
| 🟠 | **In Progress** | HACI actively investigating |
| 🟡 | **Awaiting Approval** | Needs human decision |
| 🟢 | **Complete** | Successfully resolved |
| ⚪ | **Escalated** | Handed off to human |
| 🔵 | **Human-Led** | Human driving, AI assisting |

### Quick Filters

Use the filter bar to focus your view:

- **My Approvals:** Items waiting for your decision
- **Critical Only:** High-severity investigations
- **Stalled:** No progress in >15 minutes
- **Today:** Investigations from today
- **Team:** Your team's assignments only

---

## Working with Investigations

### Viewing an Investigation

Click any investigation row to open the detail view:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ← Back    TICKET-4521: Database timeout errors           🔴 Critical  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  TICKET DETAILS                           INVESTIGATION STATUS          │
│  ─────────────────                        ────────────────────          │
│  Customer: Acme Corp (Enterprise)         Mode: Micro-Swarm             │
│  Created: 10:42 AM (38 min ago)           Phase: OBSERVE                │
│  Source: PagerDuty alert                  Iteration: 2 of 5             │
│                                           Confidence: 72%               │
│  Description:                                                           │
│  "Multiple users reporting slow queries   Agents Active:                │
│  and timeout errors starting ~10:30 AM"   • Database Agent ✅           │
│                                           • Log Agent ✅                │
│                                           • Infrastructure Agent 🔄     │
├─────────────────────────────────────────────────────────────────────────┤
│  INVESTIGATION TIMELINE                                                 │
│  ─────────────────────                                                  │
│                                                                         │
│  10:42:15  📥 Ticket received from PagerDuty                           │
│  10:42:18  🤖 Meta-orchestrator selected: Micro-Swarm mode             │
│  10:42:20  🧠 THINK: Formed 3 hypotheses                               │
│            → Connection pool exhaustion (45%)                          │
│            → Query performance regression (35%)                         │
│            → Infrastructure resource constraint (20%)                   │
│  10:42:45  ⚡ ACT: Executing 4 tool calls                              │
│            → Datadog: query_metrics ✅                                  │
│            → CloudWatch: get_rds_metrics ✅                            │
│            → GitHub: recent_deployments ✅                              │
│            → PostgreSQL: slow_query_log 🔄                             │
│  10:43:12  👁️ OBSERVE: Analyzing results...                           │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  CURRENT HYPOTHESES                                                     │
│  ──────────────────                                                     │
│                                                                         │
│  1. Connection pool exhaustion                          [72%] ████████░░│
│     Evidence: Pool at 95% capacity, 47 timeout errors                  │
│                                                                         │
│  2. Query regression from deployment                    [45%] █████░░░░░│
│     Evidence: v2.4.1 deployed 2 hours ago                              │
│                                                                         │
│  3. RDS resource constraint                             [23%] ███░░░░░░░│
│     Evidence: CPU normal, memory normal                                │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  [Take Over]  [Add Context]  [Escalate]  [View Full Trace]             │
└─────────────────────────────────────────────────────────────────────────┘
```

### Understanding the Timeline

The timeline shows every action HACI takes:

| Icon | Event Type | Description |
|------|------------|-------------|
| 📥 | Ticket Received | Investigation started |
| 🤖 | Mode Selection | Which execution mode was chosen |
| 🧠 | THINK | Hypotheses formed |
| ⚡ | ACT | Tools being executed |
| 👁️ | OBSERVE | Results being analyzed |
| ✅ | EVALUATE | Decision point reached |
| ⏸️ | Awaiting Approval | Paused for human input |
| 👤 | Human Action | Operator took action |
| 🎉 | Complete | Investigation resolved |
| 🚨 | Escalated | Handed to human |

### Adding Context

Help HACI by providing additional context:

1. Click **Add Context** on any investigation
2. Enter information HACI might not have access to:
   - "Customer mentioned they changed their firewall rules yesterday"
   - "This service was migrated to new database last week"
   - "Similar issue happened in March - check TICKET-3021"
3. Click **Submit Context**

HACI incorporates this in its next THINK phase.

### Viewing the Full Trace

For deep debugging, click **View Full Trace** to open LangSmith:

- See every LLM prompt and response
- View exact tool inputs/outputs
- Check token usage and latency
- Identify where reasoning went wrong

---

## Approval Workflows

### When Approvals Are Required

HACI requests approval when:

| Trigger | Example |
|---------|---------|
| Confidence 70-84% | "I'm 78% sure this is the cause" |
| High-severity ticket | Any critical ticket finding |
| Destructive action | Restart service, clear cache |
| Enterprise customer | Policy requires human review |
| First time for pattern | Novel issue type |

### The Approval Queue

Access via **Approvals** in the main navigation:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PENDING APPROVALS                                          [Filter ▼] │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ⏰ 12 min   TICKET-4519   API latency spike                           │
│  ──────────────────────────────────────────────────────────────────────│
│  Finding: Redis cache eviction causing repeated database hits          │
│  Confidence: 81%                                                        │
│  Proposed Action: Increase Redis maxmemory from 2GB to 4GB             │
│  Risk Level: Medium                                                     │
│                                                                         │
│  [✅ Approve]  [✅ Approve & Execute]  [❌ Reject]  [💬 Request Info]  │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  ⏰ 8 min    TICKET-4520   Login failures                              │
│  ──────────────────────────────────────────────────────────────────────│
│  Finding: Auth service memory leak after deployment                     │
│  Confidence: 74%                                                        │
│  Proposed Action: Rollback to v2.3.9                                   │
│  Risk Level: High                                                       │
│                                                                         │
│  [✅ Approve]  [✅ Approve & Execute]  [❌ Reject]  [💬 Request Info]  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Approval Actions

| Action | What Happens |
|--------|--------------|
| **Approve** | Confirms finding is correct; HACI proceeds |
| **Approve & Execute** | Confirms finding AND authorizes proposed action |
| **Reject** | Marks finding as incorrect; HACI re-investigates or escalates |
| **Request Info** | Asks HACI for more details before deciding |

### Making Good Approval Decisions

**Before approving, verify:**

1. ✅ Does the evidence support the conclusion?
2. ✅ Is the confidence level appropriate?
3. ✅ Is the proposed action proportionate to the issue?
4. ✅ Are there risks HACI might have missed?

**When to reject:**

- Evidence doesn't match conclusion
- You have information HACI doesn't
- Proposed action seems excessive
- Something feels off (trust your instincts)

**Adding rejection feedback:**

When rejecting, always explain why:
```
"Rejecting because: The customer confirmed they haven't made firewall 
changes. Please investigate application-level issues instead."
```

This helps HACI learn and improves future investigations.

### Approval SLAs

Approvals have time expectations:

| Risk Level | Expected Response | Escalation If Missed |
|------------|-------------------|----------------------|
| Low | 30 minutes | Auto-escalate to senior |
| Medium | 15 minutes | Page on-call |
| High | 5 minutes | Page on-call + manager |
| Critical | Immediate | Conference bridge |

Check the **⏰ timer** on each approval to see urgency.

---

## Monitoring & Alerts

### Notification Channels

HACI sends notifications via your configured channel:

**Slack Notifications:**
```
🔔 HACI Approval Required
━━━━━━━━━━━━━━━━━━━━━━━━
Ticket: TICKET-4519
Finding: Redis cache eviction
Confidence: 81%
Risk: Medium

[View in HACI] [Quick Approve] [Quick Reject]
```

**Email Notifications:**
- Subject: `[HACI] Approval Required: TICKET-4519`
- Includes full context and one-click action links

### Alert Types

| Alert | Priority | Meaning |
|-------|----------|---------|
| **Approval Required** | Normal | Awaiting your decision |
| **Approval Urgent** | High | SLA approaching |
| **Investigation Stalled** | Medium | No progress in 15+ min |
| **Escalation** | High | HACI couldn't resolve |
| **System Health** | Varies | HACI platform issues |

### Managing Alert Fatigue

Customize in **Settings → Notifications:**

- **Batch non-urgent:** Group low-priority alerts
- **Quiet hours:** Suppress non-critical during off-hours
- **Delegation:** Route to backup when OOO
- **Threshold adjustment:** Alert only on 2+ approvals

---

## Manual Interventions

### Taking Over an Investigation

When you need to drive manually:

1. Open the investigation
2. Click **Take Over**
3. Select reason:
   - "HACI is stuck"
   - "I have context HACI doesn't"
   - "Customer requested human"
   - "Sensitive situation"
4. The investigation switches to **Human-Led** mode

**In Human-Led mode:**
- You make all decisions
- HACI provides research assistance
- All your actions are logged
- You can return control to HACI anytime

### Using AI Assist

Even in Human-Led mode, leverage HACI:

**Ask questions:**
```
You: "What would cause connection pool exhaustion?"

HACI: "Common causes include:
1. Connection leaks (connections not being released)
2. Increased traffic without pool scaling
3. Slow queries holding connections longer
4. Network issues causing connection timeouts

Based on current evidence, I'd investigate #1 first - 
the logs show connections being opened but not closed."
```

**Request tool execution:**
```
You: "Run the slow query analysis for the last 2 hours"

HACI: "Executing PostgreSQL slow query log analysis...

Results:
- 47 queries exceeded 5s threshold
- Top offender: SELECT * FROM orders WHERE... (avg 12.3s)
- Pattern started at 10:28 AM
- All slow queries involve the 'orders' table"
```

### Escalating to Specialists

Route to human specialists:

1. Click **Escalate**
2. Select escalation type:
   - **DBA Team** - Database issues
   - **Security Team** - Security concerns
   - **Platform Team** - Infrastructure issues
   - **Application Team** - Code issues
   - **Management** - Customer escalation
3. Add context for the receiving team
4. Click **Escalate Now**

The receiving team gets full investigation history.

### Documenting Manual Actions

When you take manual actions outside HACI:

1. Click **Log Action** on the investigation
2. Record what you did:
   ```
   Action: Restarted the auth-service pod
   Reason: Memory usage at 98%, suspected leak
   Outcome: Service recovered, monitoring for recurrence
   ```
3. This becomes part of the audit trail

---

## Reporting & Analytics

### Personal Dashboard

View your performance in **Analytics → My Stats:**

| Metric | Your Value | Team Avg |
|--------|------------|----------|
| Approvals/day | 12 | 8 |
| Avg response time | 4.2 min | 6.1 min |
| Rejection rate | 8% | 12% |
| Escalation rate | 3% | 5% |

### Team Dashboard

Managers see **Analytics → Team:**

- Resolution rates by agent
- MTTR trends
- Approval queue health
- Top issue categories
- Capacity utilization

### Generating Reports

1. Go to **Analytics → Reports**
2. Select report type:
   - **Daily Summary** - Today's activity
   - **Weekly Review** - Week's performance
   - **Monthly Executive** - High-level metrics
   - **Custom** - Build your own
3. Set date range and filters
4. Click **Generate**
5. Download as PDF, CSV, or schedule recurring

### Key Metrics to Watch

| Metric | Healthy Range | Action If Outside |
|--------|---------------|-------------------|
| Auto-resolution rate | >80% | Review rejection patterns |
| Avg MTTR | <30 min | Check stalled investigations |
| Approval queue age | <10 min | Add approvers or adjust thresholds |
| Confidence calibration | ±5% | Report to HACI admin |
| Escalation rate | <10% | Review escalation reasons |

---

## Best Practices

### Do's ✅

1. **Review before approving** - Even quick glance catches errors
2. **Add context when you have it** - HACI learns from your input
3. **Provide rejection feedback** - Helps improve future accuracy
4. **Use filters effectively** - Focus on what needs attention
5. **Check the trace when uncertain** - Full reasoning visible in LangSmith
6. **Trust but verify** - HACI is good but not perfect
7. **Document manual actions** - Maintains complete audit trail
8. **Escalate early** - When stuck, escalate rather than delay

### Don'ts ❌

1. **Don't rubber-stamp approvals** - Quality matters more than speed
2. **Don't ignore stalled investigations** - They need attention
3. **Don't skip rejection feedback** - "Rejected" alone doesn't help
4. **Don't take over unnecessarily** - HACI learns from completion
5. **Don't forget to return control** - After manual intervention
6. **Don't share credentials** - Each operator has own login
7. **Don't modify findings directly** - Use proper rejection flow
8. **Don't ignore your SLAs** - Approvals have time expectations

### Handling Edge Cases

**When HACI is confident but wrong:**
1. Reject with detailed explanation
2. Provide the correct answer if known
3. Flag for review by HACI admin
4. This improves future accuracy

**When you're not sure:**
1. Request more info from HACI
2. Check the full trace for reasoning
3. Consult with colleagues
4. Escalate if still uncertain

**When customer is frustrated:**
1. Take over to add human touch
2. Use HACI for research
3. Communicate proactively
4. Log interaction for context

---

## Keyboard Shortcuts

### Global

| Shortcut | Action |
|----------|--------|
| `G` then `I` | Go to Investigations |
| `G` then `A` | Go to Approvals |
| `G` then `R` | Go to Reports |
| `/` | Focus search |
| `?` | Show all shortcuts |
| `Esc` | Close modal/panel |

### Investigation View

| Shortcut | Action |
|----------|--------|
| `J` / `K` | Next/previous investigation |
| `Enter` | Open selected investigation |
| `T` | Take over |
| `E` | Escalate |
| `C` | Add context |
| `L` | View LangSmith trace |

### Approval View

| Shortcut | Action |
|----------|--------|
| `J` / `K` | Next/previous approval |
| `A` | Approve |
| `Shift+A` | Approve & Execute |
| `R` | Reject (opens dialog) |
| `I` | Request info |

---

## Getting Help

### In-App Help

- Click **?** icon in bottom right for contextual help
- Each page has **Learn More** links to documentation
- Tooltips on hover explain elements

### Support Channels

| Issue Type | Channel | Response Time |
|------------|---------|---------------|
| How-to questions | #haci-help Slack | <1 hour |
| Bug reports | JIRA HACI project | <4 hours |
| Urgent issues | Page HACI on-call | <15 min |
| Feature requests | haci-feedback@company.com | Weekly review |

### Training Resources

- **HACI 101:** 30-minute intro course (required for all operators)
- **Advanced Approvals:** Deep dive on approval decisions
- **Power User:** Keyboard shortcuts and efficiency tips
- **Admin Training:** Configuration and management

Access all training at: `https://training.yourcompany.com/haci`

---

## Appendix: Status Reference

### Investigation Statuses

| Status | Description | Your Action |
|--------|-------------|-------------|
| `queued` | Waiting to start | None - will start soon |
| `in_progress` | Actively investigating | Monitor if interested |
| `awaiting_approval` | Needs human decision | Review and decide |
| `approved` | Approved, executing | None - in progress |
| `complete` | Successfully resolved | Review if desired |
| `escalated` | Handed to human | Take over or assign |
| `failed` | System error | Report to admin |
| `cancelled` | Manually cancelled | None |

### Confidence Levels

| Range | Label | Typical Action |
|-------|-------|----------------|
| 95-100% | Very High | Auto-execute |
| 85-94% | High | Execute + review |
| 70-84% | Medium | Require approval |
| 50-69% | Low | Require approval + extra scrutiny |
| <50% | Very Low | Likely escalate |

### Risk Levels

| Level | Examples | Approval Required |
|-------|----------|-------------------|
| **Low** | Read-only queries, status checks | No |
| **Medium** | Config changes, restarts | If confidence <90% |
| **High** | Deployments, data changes | Always |
| **Critical** | Security changes, data deletion | Always + senior |

---

*Last updated: January 2026 | Version 1.0*
