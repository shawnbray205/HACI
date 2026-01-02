# HACI API Reference

> Complete REST API documentation for HACI integration and automation

---

## Overview

### Base URL

```
Production:  https://api.haci.yourcompany.com/v1
Staging:     https://api-staging.haci.yourcompany.com/v1
Development: http://localhost:8080/v1
```

### Authentication

All API requests require authentication via Bearer token:

```bash
curl -X GET "https://api.haci.yourcompany.com/v1/investigations" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

**Obtaining a Token:**

1. Go to **HACI Dashboard → Profile → API Tokens**
2. Click **Generate New Token**
3. Set expiration and permissions
4. Copy the token (shown only once)

**Token Types:**

| Type | Use Case | Permissions |
|------|----------|-------------|
| `read` | Monitoring, reporting | Read-only access |
| `write` | Create tickets, add context | Read + create |
| `admin` | Full management | All operations |

### Rate Limits

| Endpoint Category | Limit | Window |
|-------------------|-------|--------|
| Read operations | 1000 | 1 minute |
| Write operations | 100 | 1 minute |
| Bulk operations | 10 | 1 minute |

Rate limit headers included in responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 847
X-RateLimit-Reset: 1704067200
```

### Response Format

All responses are JSON:

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2026-01-15T10:30:00Z"
  }
}
```

**Error Response:**

```json
{
  "success": false,
  "error": {
    "code": "E002",
    "message": "Investigation not found",
    "details": "No investigation exists with ID inv_xyz789"
  },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2026-01-15T10:30:00Z"
  }
}
```

### Common HTTP Status Codes

| Code | Meaning |
|------|---------|
| `200` | Success |
| `201` | Created |
| `202` | Accepted (async operation started) |
| `400` | Bad Request (invalid input) |
| `401` | Unauthorized (invalid/missing token) |
| `403` | Forbidden (insufficient permissions) |
| `404` | Not Found |
| `409` | Conflict (resource state conflict) |
| `429` | Too Many Requests (rate limited) |
| `500` | Internal Server Error |
| `503` | Service Unavailable |

---

## Investigations

### List Investigations

Retrieve a paginated list of investigations.

```
GET /investigations
```

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `status` | string | all | Filter: `active`, `complete`, `escalated`, `all` |
| `severity` | string | all | Filter: `critical`, `high`, `medium`, `low`, `all` |
| `mode` | string | all | Filter: `single_agent`, `micro_swarm`, `full_swarm`, `human_led` |
| `since` | datetime | - | Investigations created after this time (ISO 8601) |
| `until` | datetime | - | Investigations created before this time (ISO 8601) |
| `limit` | integer | 25 | Results per page (max 100) |
| `offset` | integer | 0 | Pagination offset |
| `sort` | string | `-created_at` | Sort field (prefix `-` for descending) |

**Example Request:**

```bash
curl -X GET "https://api.haci.yourcompany.com/v1/investigations?status=active&severity=critical&limit=10" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "investigations": [
      {
        "id": "inv_abc123",
        "ticket_id": "TICKET-4521",
        "ticket_source": "pagerduty",
        "title": "Database timeout errors",
        "severity": "critical",
        "status": "in_progress",
        "mode": "micro_swarm",
        "phase": "observe",
        "iteration": 2,
        "confidence": 0.72,
        "created_at": "2026-01-15T10:42:15Z",
        "updated_at": "2026-01-15T10:45:30Z",
        "agents_active": ["database_agent", "log_agent", "infrastructure_agent"],
        "url": "https://haci.yourcompany.com/investigations/inv_abc123"
      }
    ],
    "pagination": {
      "total": 47,
      "limit": 10,
      "offset": 0,
      "has_more": true
    }
  }
}
```

---

### Get Investigation

Retrieve detailed information about a specific investigation.

```
GET /investigations/{investigation_id}
```

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `investigation_id` | string | Investigation ID (e.g., `inv_abc123`) |

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `include` | string | - | Comma-separated: `timeline`, `hypotheses`, `evidence`, `trace` |

**Example Request:**

```bash
curl -X GET "https://api.haci.yourcompany.com/v1/investigations/inv_abc123?include=timeline,hypotheses" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "id": "inv_abc123",
    "ticket_id": "TICKET-4521",
    "ticket_source": "pagerduty",
    "title": "Database timeout errors",
    "description": "Multiple users reporting slow queries and timeout errors starting ~10:30 AM",
    "severity": "critical",
    "status": "in_progress",
    "mode": "micro_swarm",
    "phase": "observe",
    "iteration": 2,
    "max_iterations": 5,
    "confidence": 0.72,
    "created_at": "2026-01-15T10:42:15Z",
    "updated_at": "2026-01-15T10:45:30Z",
    "customer": {
      "id": "cust_xyz",
      "name": "Acme Corp",
      "tier": "enterprise"
    },
    "agents_active": ["database_agent", "log_agent", "infrastructure_agent"],
    "current_finding": "Connection pool exhaustion due to connection leaks",
    "proposed_action": null,
    "timeline": [
      {
        "timestamp": "2026-01-15T10:42:15Z",
        "event": "investigation_started",
        "details": {"source": "pagerduty", "alert_id": "P123ABC"}
      },
      {
        "timestamp": "2026-01-15T10:42:18Z",
        "event": "mode_selected",
        "details": {"mode": "micro_swarm", "agents": ["database_agent", "log_agent", "infrastructure_agent"]}
      },
      {
        "timestamp": "2026-01-15T10:42:20Z",
        "event": "phase_started",
        "details": {"phase": "think", "iteration": 1}
      },
      {
        "timestamp": "2026-01-15T10:42:35Z",
        "event": "hypotheses_formed",
        "details": {"count": 3}
      }
    ],
    "hypotheses": [
      {
        "id": "hyp_001",
        "statement": "Connection pool exhaustion causing timeouts",
        "confidence": 0.72,
        "evidence_for": ["Pool at 95% capacity", "47 timeout errors in last hour"],
        "evidence_against": []
      },
      {
        "id": "hyp_002",
        "statement": "Query regression from v2.4.1 deployment",
        "confidence": 0.45,
        "evidence_for": ["Deployment 45 minutes before issue"],
        "evidence_against": ["No slow query pattern change"]
      }
    ],
    "trace_url": "https://smith.langchain.com/runs/abc123"
  }
}
```

---

### Create Investigation

Manually trigger a new investigation.

```
POST /investigations
```

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Brief description of the issue |
| `description` | string | Yes | Detailed description |
| `severity` | string | Yes | `critical`, `high`, `medium`, `low` |
| `source` | string | No | Origin system (default: `api`) |
| `source_id` | string | No | External ticket/alert ID |
| `customer_id` | string | No | Associated customer |
| `mode` | string | No | Force mode: `single_agent`, `micro_swarm`, `full_swarm`, `human_led` |
| `context` | object | No | Additional context for investigation |
| `priority` | boolean | No | Jump to front of queue (default: false) |

**Example Request:**

```bash
curl -X POST "https://api.haci.yourcompany.com/v1/investigations" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "API latency spike detected",
    "description": "P95 latency increased from 200ms to 2s starting at 14:00 UTC",
    "severity": "high",
    "source": "datadog",
    "source_id": "alert_12345",
    "customer_id": "cust_xyz",
    "context": {
      "affected_endpoints": ["/api/v2/orders", "/api/v2/users"],
      "region": "us-east-1"
    }
  }'
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "id": "inv_def456",
    "status": "queued",
    "message": "Investigation created and queued for processing",
    "url": "https://haci.yourcompany.com/investigations/inv_def456"
  }
}
```

---

### Add Context to Investigation

Provide additional context to an active investigation.

```
POST /investigations/{investigation_id}/context
```

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `context` | string | Yes | Human-readable context to add |
| `structured_data` | object | No | Machine-readable data |

**Example Request:**

```bash
curl -X POST "https://api.haci.yourcompany.com/v1/investigations/inv_abc123/context" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "context": "Customer mentioned they deployed a database migration at 10:15 AM",
    "structured_data": {
      "deployment_time": "2026-01-15T10:15:00Z",
      "deployment_type": "database_migration"
    }
  }'
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "message": "Context added successfully",
    "will_apply_at": "next_think_phase"
  }
}
```

---

### Escalate Investigation

Manually escalate an investigation to human operators.

```
POST /investigations/{investigation_id}/escalate
```

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `reason` | string | Yes | Reason for escalation |
| `target_team` | string | No | Team to escalate to |
| `priority` | string | No | `normal`, `urgent` (default: `normal`) |

**Example Request:**

```bash
curl -X POST "https://api.haci.yourcompany.com/v1/investigations/inv_abc123/escalate" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "Customer requested human contact",
    "target_team": "tier2_support",
    "priority": "urgent"
  }'
```

---

### Cancel Investigation

Cancel an in-progress investigation.

```
POST /investigations/{investigation_id}/cancel
```

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `reason` | string | Yes | Reason for cancellation |

---

## Approvals

### List Pending Approvals

Get all approvals awaiting action.

```
GET /approvals
```

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `status` | string | `pending` | Filter: `pending`, `approved`, `rejected`, `expired`, `all` |
| `assignee` | string | - | Filter by assignee user ID |
| `risk_level` | string | all | Filter: `low`, `medium`, `high`, `critical` |
| `limit` | integer | 25 | Results per page |
| `offset` | integer | 0 | Pagination offset |

**Example Response:**

```json
{
  "success": true,
  "data": {
    "approvals": [
      {
        "id": "apr_xyz789",
        "investigation_id": "inv_abc123",
        "ticket_id": "TICKET-4521",
        "type": "finding_approval",
        "status": "pending",
        "risk_level": "medium",
        "created_at": "2026-01-15T10:45:00Z",
        "expires_at": "2026-01-15T11:00:00Z",
        "time_remaining_seconds": 542,
        "finding": {
          "summary": "Redis cache eviction causing repeated database hits",
          "confidence": 0.81,
          "evidence_count": 4
        },
        "proposed_action": {
          "description": "Increase Redis maxmemory from 2GB to 4GB",
          "risk_level": "medium",
          "reversible": true
        },
        "assignees": ["user_123", "user_456"],
        "url": "https://haci.yourcompany.com/approvals/apr_xyz789"
      }
    ],
    "pagination": {
      "total": 3,
      "limit": 25,
      "offset": 0,
      "has_more": false
    }
  }
}
```

---

### Get Approval Details

```
GET /approvals/{approval_id}
```

Returns full approval details including investigation context, evidence, and proposed actions.

---

### Approve

Approve a pending approval request.

```
POST /approvals/{approval_id}/approve
```

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `execute_action` | boolean | No | Also execute proposed action (default: false) |
| `comment` | string | No | Approval comment for audit trail |

**Example Request:**

```bash
curl -X POST "https://api.haci.yourcompany.com/v1/approvals/apr_xyz789/approve" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "execute_action": true,
    "comment": "Verified evidence looks correct. Approved."
  }'
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "approval_id": "apr_xyz789",
    "status": "approved",
    "action_status": "executing",
    "approved_by": "user_123",
    "approved_at": "2026-01-15T10:52:30Z"
  }
}
```

---

### Reject

Reject a pending approval request.

```
POST /approvals/{approval_id}/reject
```

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `reason` | string | Yes | Reason for rejection |
| `action` | string | No | `reinvestigate`, `escalate`, `close` (default: `reinvestigate`) |
| `guidance` | string | No | Guidance for re-investigation |

**Example Request:**

```bash
curl -X POST "https://api.haci.yourcompany.com/v1/approvals/apr_xyz789/reject" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "Evidence does not support conclusion. Customer has not changed Redis config.",
    "action": "reinvestigate",
    "guidance": "Check application-level caching instead"
  }'
```

---

### Reassign Approval

Reassign an approval to different users.

```
POST /approvals/{approval_id}/reassign
```

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `assignees` | array | Yes | List of user IDs |
| `reason` | string | No | Reason for reassignment |

---

## Agents

### List Agents

Get all available agents and their status.

```
GET /agents
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "agents": [
      {
        "id": "log_agent",
        "name": "Log Agent",
        "description": "Analyzes application and system logs",
        "status": "available",
        "capabilities": ["log_search", "pattern_detection", "anomaly_detection"],
        "tools": ["datadog_logs", "splunk_search", "cloudwatch_logs"],
        "current_load": 3,
        "max_concurrent": 10,
        "avg_investigation_time_seconds": 180
      },
      {
        "id": "database_agent",
        "name": "Database Agent",
        "description": "Investigates database performance and issues",
        "status": "available",
        "capabilities": ["query_analysis", "connection_monitoring", "schema_review"],
        "tools": ["postgresql_metrics", "mysql_slow_query", "mongodb_profiler"],
        "current_load": 1,
        "max_concurrent": 5,
        "avg_investigation_time_seconds": 240
      }
    ]
  }
}
```

---

### Get Agent Details

```
GET /agents/{agent_id}
```

Returns detailed agent information including configuration, recent performance metrics, and tool availability.

---

### Get Agent Metrics

```
GET /agents/{agent_id}/metrics
```

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `period` | string | `24h` | Time period: `1h`, `24h`, `7d`, `30d` |

**Example Response:**

```json
{
  "success": true,
  "data": {
    "agent_id": "log_agent",
    "period": "24h",
    "metrics": {
      "investigations_completed": 127,
      "avg_confidence": 0.84,
      "avg_duration_seconds": 185,
      "accuracy_rate": 0.91,
      "escalation_rate": 0.06,
      "tool_success_rate": 0.97
    }
  }
}
```

---

## Tools

### List Tools

Get all configured tools and their status.

```
GET /tools
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "tools": [
      {
        "id": "datadog_logs",
        "name": "Datadog Log Search",
        "type": "mcp",
        "status": "healthy",
        "last_check": "2026-01-15T10:50:00Z",
        "avg_latency_ms": 450,
        "success_rate_24h": 0.98
      },
      {
        "id": "github_search",
        "name": "GitHub Code Search",
        "type": "api",
        "status": "healthy",
        "last_check": "2026-01-15T10:50:00Z",
        "avg_latency_ms": 320,
        "success_rate_24h": 0.99
      }
    ]
  }
}
```

---

### Test Tool

Test a specific tool's connectivity and functionality.

```
POST /tools/{tool_id}/test
```

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `test_args` | object | No | Arguments for test invocation |

**Example Request:**

```bash
curl -X POST "https://api.haci.yourcompany.com/v1/tools/datadog_logs/test" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "test_args": {
      "query": "status:error",
      "timeframe": "15m"
    }
  }'
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "tool_id": "datadog_logs",
    "status": "healthy",
    "latency_ms": 423,
    "result_preview": "Found 47 matching log entries",
    "tested_at": "2026-01-15T10:55:00Z"
  }
}
```

---

### Execute Tool

Manually execute a tool (admin only).

```
POST /tools/{tool_id}/execute
```

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `args` | object | Yes | Tool arguments |
| `context` | string | No | Reason for execution |

---

## Metrics & Analytics

### Get System Metrics

```
GET /metrics/system
```

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `period` | string | `24h` | Time period |

**Example Response:**

```json
{
  "success": true,
  "data": {
    "period": "24h",
    "investigations": {
      "total": 312,
      "by_status": {
        "complete": 287,
        "in_progress": 18,
        "escalated": 7
      },
      "by_mode": {
        "single_agent": 198,
        "micro_swarm": 89,
        "full_swarm": 22,
        "human_led": 3
      }
    },
    "performance": {
      "avg_mttr_seconds": 1320,
      "p50_mttr_seconds": 840,
      "p95_mttr_seconds": 3600,
      "auto_resolution_rate": 0.85,
      "avg_confidence": 0.86
    },
    "approvals": {
      "total": 47,
      "approved": 41,
      "rejected": 6,
      "avg_response_time_seconds": 312
    }
  }
}
```

---

### Get Resolution Metrics

```
GET /metrics/resolutions
```

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `period` | string | `7d` | Time period |
| `group_by` | string | `day` | Grouping: `hour`, `day`, `week` |

---

### Get Cost Metrics

```
GET /metrics/costs
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "period": "24h",
    "total_cost_usd": 47.23,
    "by_provider": {
      "anthropic": 28.50,
      "openai": 12.30,
      "google": 6.43
    },
    "by_model": {
      "claude-sonnet-4": 25.20,
      "claude-haiku-3": 3.30,
      "gpt-4o": 10.80,
      "gemini-flash": 6.43
    },
    "avg_cost_per_investigation": 0.15,
    "token_usage": {
      "input_tokens": 2847000,
      "output_tokens": 892000
    }
  }
}
```

---

## Webhooks

### List Webhooks

```
GET /webhooks
```

### Create Webhook

Register a webhook to receive HACI events.

```
POST /webhooks
```

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string | Yes | HTTPS endpoint URL |
| `events` | array | Yes | Events to subscribe to |
| `secret` | string | No | Signing secret (auto-generated if not provided) |
| `enabled` | boolean | No | Active state (default: true) |

**Available Events:**

| Event | Description |
|-------|-------------|
| `investigation.created` | New investigation started |
| `investigation.completed` | Investigation resolved |
| `investigation.escalated` | Investigation escalated |
| `investigation.failed` | Investigation failed |
| `approval.required` | Approval needed |
| `approval.approved` | Approval granted |
| `approval.rejected` | Approval denied |
| `approval.expired` | Approval timed out |
| `system.health` | System health change |

**Example Request:**

```bash
curl -X POST "https://api.haci.yourcompany.com/v1/webhooks" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-app.com/webhooks/haci",
    "events": ["investigation.completed", "approval.required"],
    "secret": "whsec_your_secret_key"
  }'
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "id": "whk_abc123",
    "url": "https://your-app.com/webhooks/haci",
    "events": ["investigation.completed", "approval.required"],
    "secret": "whsec_your_secret_key",
    "enabled": true,
    "created_at": "2026-01-15T11:00:00Z"
  }
}
```

---

### Webhook Payload Format

All webhook payloads follow this structure:

```json
{
  "id": "evt_xyz789",
  "type": "investigation.completed",
  "created_at": "2026-01-15T11:05:00Z",
  "data": {
    "investigation_id": "inv_abc123",
    "ticket_id": "TICKET-4521",
    "status": "complete",
    "finding": "Connection pool exhaustion due to connection leaks",
    "confidence": 0.92,
    "duration_seconds": 1247
  }
}
```

**Verifying Webhook Signatures:**

```python
import hmac
import hashlib

def verify_webhook(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)

# Usage
is_valid = verify_webhook(
    request.body,
    request.headers["X-HACI-Signature"],
    "whsec_your_secret_key"
)
```

---

### Update Webhook

```
PATCH /webhooks/{webhook_id}
```

### Delete Webhook

```
DELETE /webhooks/{webhook_id}
```

### Test Webhook

Send a test event to verify webhook configuration.

```
POST /webhooks/{webhook_id}/test
```

---

## Health & Status

### Health Check

```
GET /health
```

**Example Response:**

```json
{
  "status": "healthy",
  "version": "2.4.1",
  "timestamp": "2026-01-15T11:10:00Z",
  "components": {
    "api": "healthy",
    "database": "healthy",
    "redis": "healthy",
    "llm_providers": "healthy",
    "queue": "healthy"
  }
}
```

---

### Detailed Status

```
GET /status
```

Returns detailed status of all system components including queue depth, active investigations, and provider availability.

---

## SDK Examples

### Python SDK

```python
from haci import HACIClient

# Initialize
client = HACIClient(
    api_key="YOUR_API_TOKEN",
    base_url="https://api.haci.yourcompany.com/v1"
)

# Create investigation
investigation = client.investigations.create(
    title="API latency spike",
    description="P95 latency increased from 200ms to 2s",
    severity="high"
)
print(f"Created: {investigation.id}")

# Wait for completion
result = client.investigations.wait_for_completion(
    investigation.id,
    timeout=300
)
print(f"Finding: {result.finding}")
print(f"Confidence: {result.confidence}")

# List pending approvals
approvals = client.approvals.list(status="pending")
for approval in approvals:
    print(f"Pending: {approval.id} - {approval.finding.summary}")

# Approve
client.approvals.approve(
    approval_id="apr_xyz789",
    execute_action=True,
    comment="Looks good"
)
```

### JavaScript/TypeScript SDK

```typescript
import { HACIClient } from '@haci/sdk';

const client = new HACIClient({
  apiKey: 'YOUR_API_TOKEN',
  baseUrl: 'https://api.haci.yourcompany.com/v1'
});

// Create investigation
const investigation = await client.investigations.create({
  title: 'API latency spike',
  description: 'P95 latency increased from 200ms to 2s',
  severity: 'high'
});

console.log(`Created: ${investigation.id}`);

// Subscribe to updates via webhook or polling
const result = await client.investigations.waitForCompletion(
  investigation.id,
  { timeout: 300000 }
);

console.log(`Finding: ${result.finding}`);
```

### cURL Examples

```bash
# List active investigations
curl -X GET "https://api.haci.yourcompany.com/v1/investigations?status=active" \
  -H "Authorization: Bearer $HACI_TOKEN"

# Get specific investigation
curl -X GET "https://api.haci.yourcompany.com/v1/investigations/inv_abc123" \
  -H "Authorization: Bearer $HACI_TOKEN"

# Create investigation
curl -X POST "https://api.haci.yourcompany.com/v1/investigations" \
  -H "Authorization: Bearer $HACI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test issue", "description": "Testing API", "severity": "low"}'

# Approve with action
curl -X POST "https://api.haci.yourcompany.com/v1/approvals/apr_xyz789/approve" \
  -H "Authorization: Bearer $HACI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"execute_action": true}'
```

---

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `E001` | 500 | Internal server error |
| `E002` | 404 | Resource not found |
| `E003` | 400 | Invalid request body |
| `E004` | 401 | Authentication failed |
| `E005` | 403 | Insufficient permissions |
| `E006` | 409 | Resource conflict |
| `E007` | 429 | Rate limit exceeded |
| `E008` | 422 | Validation error |
| `E009` | 503 | Service unavailable |
| `E010` | 504 | Timeout |

---

## Changelog

### v1.2.0 (2026-01-15)
- Added `/metrics/costs` endpoint
- Added webhook signature verification
- Added `include` parameter to investigation details

### v1.1.0 (2025-12-01)
- Added `/agents/{id}/metrics` endpoint
- Added bulk approval endpoints
- Improved error messages

### v1.0.0 (2025-10-15)
- Initial API release

---

## Support

- **API Status:** https://status.haci.yourcompany.com
- **Documentation:** https://docs.haci.yourcompany.com
- **Support:** api-support@haci.yourcompany.com

---

*Last updated: January 2026 | API Version: 1.2.0*
