# HACI Troubleshooting Guide

> Diagnose and resolve common HACI issues quickly

---

## Quick Diagnosis

### Symptom Lookup Table

| Symptom | Likely Cause | Jump To |
|---------|--------------|---------|
| Investigation stuck/not progressing | Tool timeout, LLM issue, or loop | [Stalled Investigations](#stalled-investigations) |
| "Awaiting Approval" but no notification | Notification config or delivery | [Notification Issues](#notification-issues) |
| Low confidence on obvious issues | Missing context or tool access | [Accuracy Issues](#accuracy-issues) |
| Dashboard not loading | Browser or API issue | [UI Issues](#ui-issues) |
| Tools returning errors | Integration or credential issue | [Tool Failures](#tool-failures) |
| High latency/slow responses | LLM provider or infrastructure | [Performance Issues](#performance-issues) |
| Login/authentication problems | SSO or session issue | [Authentication Issues](#authentication-issues) |
| Approvals timing out | Queue backup or routing | [Approval Workflow Issues](#approval-workflow-issues) |

---

## Stalled Investigations

### Symptoms
- Investigation shows "In Progress" for >15 minutes
- Progress indicator not advancing
- No new timeline entries

### Diagnosis Steps

**Step 1: Check the Current Phase**

Open the investigation and note the current phase:

| Stuck In | Likely Cause |
|----------|--------------|
| THINK | LLM timeout or error |
| ACT | Tool execution timeout |
| OBSERVE | LLM processing large results |
| EVALUATE | Decision loop or LLM error |

**Step 2: Check the Timeline**

Look at the last timeline entry:
- If it shows a tool call with 🔄 (spinning), the tool is hung
- If it shows an LLM call, the model may be slow/failed

**Step 3: Check System Health**

Go to **⚙️ Settings → System Health**:
- ✅ All green = likely tool-specific issue
- 🟡 Yellow = degraded performance
- 🔴 Red = system issue, check alerts

### Solutions

#### Solution 1: Retry the Current Phase

1. Open the stalled investigation
2. Click **⚙️ Actions → Retry Current Phase**
3. HACI re-executes from the current phase
4. Monitor for 2-3 minutes

#### Solution 2: Skip Failed Tool

If a specific tool is failing:

1. Click **View Full Trace** to identify the failing tool
2. Click **⚙️ Actions → Skip Tool**
3. Select the problematic tool
4. HACI continues without that tool's data

#### Solution 3: Force Advance

If stuck in a loop:

1. Click **⚙️ Actions → Force Advance**
2. This moves to EVALUATE with current data
3. May result in lower confidence or escalation

#### Solution 4: Take Over

If nothing else works:

1. Click **Take Over**
2. Complete the investigation manually
3. Report the issue to HACI admin

### Prevention

- Monitor tool health dashboards
- Set appropriate timeouts for slow tools
- Configure fallback tools for critical integrations

---

## Tool Failures

### Symptoms
- Timeline shows ❌ on tool calls
- Error messages in tool results
- Investigation progressing but missing data

### Common Error Messages

#### "Connection refused" / "Connection timeout"

**Cause:** Target system unreachable

**Solutions:**
1. Verify the target system is up
2. Check network connectivity from HACI
3. Verify firewall rules allow HACI access
4. Check if VPN/proxy is required

```bash
# Test from HACI container
kubectl exec -it haci-api-xxx -- curl -v https://api.datadog.com/health
```

#### "401 Unauthorized" / "403 Forbidden"

**Cause:** Invalid or expired credentials

**Solutions:**
1. Go to **⚙️ Settings → Integrations**
2. Find the affected integration
3. Click **Test Connection**
4. If failed, click **Reconfigure**
5. Enter updated credentials
6. Click **Save & Test**

#### "429 Too Many Requests"

**Cause:** Rate limit exceeded

**Solutions:**
1. Check if multiple investigations are hitting same API
2. Reduce tool concurrency in settings
3. Implement/adjust rate limiting in tool config
4. Contact vendor about rate limit increase

```yaml
# config/tools/datadog.yaml
rate_limit:
  requests_per_minute: 60
  retry_after_429: true
  backoff_multiplier: 2
```

#### "500 Internal Server Error"

**Cause:** Target system error

**Solutions:**
1. Check target system's status page
2. Retry in a few minutes
3. Check target system logs
4. Contact target system support if persistent

#### "Tool not found"

**Cause:** Tool misconfigured or disabled

**Solutions:**
1. Go to **⚙️ Settings → Tools**
2. Verify the tool is enabled
3. Check tool configuration
4. Restart HACI if recently added

### Testing Tools

**Test individual tool:**
```bash
# Via HACI CLI
haci tool test datadog_search_logs --query "error" --timeframe "1h"

# Via API
curl -X POST https://haci.company.com/api/v1/tools/test \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"tool": "datadog_search_logs", "args": {"query": "error"}}'
```

**Test all tools:**
```bash
haci tools test-all --report
```

---

## Notification Issues

### Symptoms
- Approvals pending but no notification received
- Delayed notifications
- Notifications going to wrong channel

### Diagnosis

**Step 1: Check Notification Logs**

Go to **⚙️ Settings → Notifications → Logs**

Look for:
- ✅ Delivered successfully
- ❌ Delivery failed (see error)
- ⏳ Pending delivery

**Step 2: Verify Configuration**

Go to **👤 Profile → Notification Settings**

Verify:
- Correct Slack channel/email
- Notification types enabled
- Quiet hours not active

### Solutions

#### Slack Notifications Not Working

1. **Check Slack app installation:**
   - Go to Slack → Apps → HACI
   - Verify app is installed in workspace
   - Check app permissions

2. **Check channel membership:**
   - HACI bot must be in the channel
   - Invite with `/invite @HACI`

3. **Check DM permissions:**
   - Open DM with HACI bot
   - Send a test message
   - If no response, reinstall app

4. **Test notification:**
   ```bash
   haci notify test --channel "#your-channel"
   ```

#### Email Notifications Not Working

1. **Check spam/junk folder**

2. **Verify email configuration:**
   ```bash
   haci config get notifications.email
   ```

3. **Check SMTP settings:**
   - Go to **⚙️ Settings → Email**
   - Click **Send Test Email**

4. **Check email service logs:**
   ```bash
   kubectl logs -l app=haci-notifications | grep email
   ```

#### Delayed Notifications

1. **Check notification queue:**
   ```bash
   haci notifications queue status
   ```

2. **If backlogged, scale up workers:**
   ```bash
   kubectl scale deployment haci-notifications --replicas=3
   ```

3. **Check Redis connectivity:**
   ```bash
   kubectl exec -it haci-api-xxx -- redis-cli ping
   ```

---

## Accuracy Issues

### Symptoms
- Low confidence on issues that seem obvious
- Incorrect hypotheses being formed
- Missing obvious evidence

### Diagnosis

**Step 1: Review the Trace**

Click **View Full Trace** and examine:
- What context was provided to the LLM?
- What tools were called?
- What data was returned?

**Step 2: Identify the Gap**

Common causes:
| Symptom | Likely Gap |
|---------|------------|
| Obvious log entries missed | Log search query too narrow |
| Context not understood | Missing customer context |
| Historical pattern missed | Knowledge base not indexed |
| Wrong tool used | Tool selection prompt needs tuning |

### Solutions

#### Solution 1: Add Missing Context

1. Click **Add Context** on the investigation
2. Provide information HACI is missing
3. HACI incorporates in next iteration

**Good context examples:**
- "Customer is on legacy v1 API, not v2"
- "This service was just migrated from us-east-1"
- "Check TICKET-3456, same issue last month"

#### Solution 2: Improve Tool Access

If HACI can't find relevant data:

1. Check tool permissions
2. Verify search queries are appropriate
3. Expand time ranges if needed
4. Add additional data sources

#### Solution 3: Update Knowledge Base

For recurring accuracy issues:

1. Go to **⚙️ Settings → Knowledge**
2. Add runbooks, architecture docs, or historical context
3. HACI will use in future investigations

#### Solution 4: Tune Agent Prompts

For systematic issues (admin only):

1. Go to **⚙️ Settings → Agents → [Agent Name]**
2. Review system prompt
3. Add guidance for the specific pattern
4. Test with historical tickets

---

## Performance Issues

### Symptoms
- Slow page loads
- Long investigation start times
- High latency on tool calls
- Timeout errors

### Diagnosis

**Step 1: Check System Metrics**

Go to **⚙️ Settings → System Health → Metrics**

Key metrics:
| Metric | Healthy | Degraded | Critical |
|--------|---------|----------|----------|
| API latency p95 | <500ms | 500-2000ms | >2000ms |
| LLM latency p95 | <5s | 5-15s | >15s |
| Tool latency p95 | <10s | 10-30s | >30s |
| Queue depth | <100 | 100-500 | >500 |
| Error rate | <1% | 1-5% | >5% |

**Step 2: Identify Bottleneck**

```bash
# Check pod resource usage
kubectl top pods -l app=haci

# Check database connections
kubectl exec -it haci-db-0 -- psql -c "SELECT count(*) FROM pg_stat_activity"

# Check Redis memory
kubectl exec -it haci-redis-0 -- redis-cli info memory
```

### Solutions

#### High API Latency

1. **Scale API pods:**
   ```bash
   kubectl scale deployment haci-api --replicas=5
   ```

2. **Check database query performance:**
   ```sql
   SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;
   ```

3. **Add database indexes if needed**

#### High LLM Latency

1. **Check LLM provider status:**
   - https://status.anthropic.com
   - https://status.openai.com

2. **Switch to faster model for non-critical:**
   ```yaml
   # config/llm.yaml
   default_model: claude-3-haiku  # Faster than Sonnet
   ```

3. **Enable response streaming:**
   ```yaml
   streaming: true
   ```

#### High Tool Latency

1. **Increase tool timeout:**
   ```yaml
   tools:
     datadog:
       timeout: 60s  # Up from 30s
   ```

2. **Enable tool result caching:**
   ```yaml
   tools:
     datadog:
       cache_ttl: 300s
   ```

3. **Run slow tools in parallel:**
   ```yaml
   tools:
     execution:
       max_parallel: 5
   ```

#### Queue Backup

1. **Scale workers:**
   ```bash
   kubectl scale deployment haci-worker --replicas=10
   ```

2. **Clear stale jobs:**
   ```bash
   haci queue clear --older-than 1h --status failed
   ```

3. **Check for poison messages:**
   ```bash
   haci queue inspect --failed --limit 10
   ```

---

## UI Issues

### Symptoms
- Dashboard not loading
- Blank pages
- JavaScript errors
- Outdated data

### Solutions

#### Dashboard Not Loading

1. **Hard refresh:**
   - Chrome/Edge: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
   - Firefox: `Ctrl+F5`

2. **Clear browser cache:**
   - Open DevTools (F12)
   - Right-click refresh button
   - Select "Empty Cache and Hard Reload"

3. **Try incognito/private mode**

4. **Check browser console for errors (F12 → Console)**

#### Data Not Updating

1. **Check WebSocket connection:**
   - Open DevTools → Network → WS
   - Should show active connection to `/ws`

2. **Reconnect WebSocket:**
   - Click your profile → **Reconnect**

3. **Verify API health:**
   ```bash
   curl https://haci.company.com/api/health
   ```

#### Specific Elements Not Working

1. **Disable browser extensions** (especially ad blockers)

2. **Check for JavaScript errors:**
   - Open DevTools → Console
   - Look for red error messages
   - Report specific errors to support

3. **Try different browser**

---

## Authentication Issues

### Symptoms
- Cannot log in
- Session expired unexpectedly
- SSO redirect failures

### Solutions

#### SSO Login Failing

1. **Check SSO provider status**
   - Okta: status.okta.com
   - Azure AD: status.azure.com

2. **Clear SSO cookies:**
   - Clear cookies for both HACI and SSO provider domains

3. **Try direct login (if available):**
   - Navigate to `/login?method=password`

4. **Check SSO configuration (admin):**
   ```bash
   haci config get auth.sso
   ```

#### Session Expiring Too Fast

1. **Check session timeout setting:**
   - **⚙️ Settings → Security → Session Timeout**

2. **Verify "Remember Me" is checked on login**

3. **Check for clock skew:**
   - Your device time should match server time

#### Account Locked

1. **Wait 15 minutes** for automatic unlock

2. **Contact admin** for immediate unlock:
   ```bash
   haci user unlock your.email@company.com
   ```

3. **Reset password** if needed

---

## Approval Workflow Issues

### Symptoms
- Approvals not routing to correct person
- Approval SLAs being missed
- Cannot approve/reject

### Diagnosis

**Check approval routing:**
```bash
haci approvals routing show --ticket TICKET-1234
```

**Check approver availability:**
```bash
haci approvals who-can-approve --ticket TICKET-1234
```

### Solutions

#### Wrong Approver Assigned

1. **Check team assignments:**
   - **⚙️ Settings → Teams → [Team] → Members**

2. **Check routing rules:**
   - **⚙️ Settings → Approval Routing**
   - Verify rules match expected behavior

3. **Reassign manually:**
   - Open approval
   - Click **Reassign**
   - Select correct approver

#### Cannot Approve

1. **Verify your role:**
   - Must be Operator or higher
   - Must be assigned or have permission

2. **Check if already approved/rejected:**
   - May have been handled by another approver

3. **Check for technical errors:**
   - Look for error toast/message
   - Check browser console

#### Approvals Backing Up

1. **Check approver availability:**
   - Are approvers online?
   - Check OOO calendar

2. **Escalate overdue approvals:**
   ```bash
   haci approvals escalate --overdue-by 15m
   ```

3. **Adjust auto-escalation rules:**
   - **⚙️ Settings → Approvals → Auto-Escalation**

---

## Integration-Specific Issues

### Datadog

| Error | Solution |
|-------|----------|
| "Invalid API Key" | Regenerate key in Datadog → Organization Settings → API Keys |
| "No data returned" | Check query syntax; verify logs exist in timeframe |
| "Rate limited" | Reduce query frequency or upgrade Datadog plan |

### PagerDuty

| Error | Solution |
|-------|----------|
| "Invalid token" | Generate new token: PagerDuty → API Access Keys |
| "Service not found" | Verify service ID in HACI config |
| "Cannot create incident" | Check integration permissions |

### Jira

| Error | Solution |
|-------|----------|
| "Authentication failed" | Use API token, not password: Atlassian → API Tokens |
| "Project not found" | Check project key (e.g., "PROJ" not "Project Name") |
| "Field not found" | Verify custom fields exist and are accessible |

### Slack

| Error | Solution |
|-------|----------|
| "channel_not_found" | Invite HACI bot to channel |
| "not_in_channel" | Reinstall Slack app |
| "invalid_auth" | Regenerate bot token |

### AWS

| Error | Solution |
|-------|----------|
| "AccessDenied" | Check IAM role/policy attached to HACI |
| "ExpiredToken" | If using STS, tokens refresh automatically; check IAM role |
| "UnauthorizedAccess" | Verify HACI role can assume required roles |

---

## System Health Checks

### Daily Health Check

Run these checks daily or set up automated monitoring:

```bash
# 1. Check all services are running
kubectl get pods -l app=haci

# 2. Check API health
curl https://haci.company.com/api/health

# 3. Check queue health
haci queue status

# 4. Check integration health
haci integrations test-all

# 5. Check recent errors
haci logs errors --last 1h --summary
```

### Automated Health Script

```bash
#!/bin/bash
# haci-health-check.sh

echo "=== HACI Health Check ==="

# API Health
API_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://haci.company.com/api/health)
if [ "$API_STATUS" = "200" ]; then
    echo "✅ API: Healthy"
else
    echo "❌ API: Unhealthy (HTTP $API_STATUS)"
fi

# Database
DB_STATUS=$(kubectl exec haci-api-0 -- pg_isready -h haci-db)
if [ $? -eq 0 ]; then
    echo "✅ Database: Connected"
else
    echo "❌ Database: Connection failed"
fi

# Redis
REDIS_STATUS=$(kubectl exec haci-api-0 -- redis-cli -h haci-redis ping)
if [ "$REDIS_STATUS" = "PONG" ]; then
    echo "✅ Redis: Connected"
else
    echo "❌ Redis: Connection failed"
fi

# Queue Depth
QUEUE_DEPTH=$(haci queue status --format json | jq '.depth')
if [ "$QUEUE_DEPTH" -lt 100 ]; then
    echo "✅ Queue: Healthy ($QUEUE_DEPTH pending)"
else
    echo "⚠️ Queue: Backlog ($QUEUE_DEPTH pending)"
fi

# LLM Providers
for provider in anthropic openai google; do
    STATUS=$(haci llm test $provider --timeout 5s 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "✅ LLM ($provider): Available"
    else
        echo "⚠️ LLM ($provider): Unavailable"
    fi
done
```

---

## Getting Help

### Before Contacting Support

Gather this information:

1. **Investigation ID** (if applicable)
2. **Timestamp** when issue occurred
3. **Screenshots** of error messages
4. **Browser** and version
5. **Steps to reproduce**

### Support Channels

| Severity | Channel | Response |
|----------|---------|----------|
| **P1 - Critical** | Page on-call: `haci-oncall@company.com` | 15 min |
| **P2 - High** | Slack: `#haci-support` | 1 hour |
| **P3 - Medium** | Email: `haci-support@company.com` | 4 hours |
| **P4 - Low** | Jira: `HACI` project | 1 business day |

### Useful Log Commands

```bash
# Get recent API logs
kubectl logs -l app=haci-api --since 1h | tail -100

# Get logs for specific investigation
haci logs investigation TICKET-1234

# Get error summary
haci logs errors --last 24h --group-by type

# Export logs for support ticket
haci logs export --last 1h --output haci-logs.tar.gz
```

---

## Appendix: Error Code Reference

| Code | Meaning | Resolution |
|------|---------|------------|
| `E001` | LLM provider error | Check provider status, retry |
| `E002` | Tool execution failed | Check tool configuration |
| `E003` | Database connection error | Check DB connectivity |
| `E004` | Redis connection error | Check Redis connectivity |
| `E005` | Authentication failed | Re-authenticate |
| `E006` | Authorization denied | Check permissions |
| `E007` | Rate limit exceeded | Wait and retry |
| `E008` | Timeout | Increase timeout or optimize |
| `E009` | Invalid configuration | Check config file syntax |
| `E010` | Resource not found | Verify ID/path exists |
| `E011` | Validation error | Check input format |
| `E012` | Conflict | Resource modified concurrently |
| `E013` | Service unavailable | Check system health |
| `E014` | Integration error | Check integration config |
| `E015` | Checkpoint error | Check PostgreSQL |

---

*Last updated: January 2026 | Version 1.0*
