# HACI Integration Cookbooks

> Step-by-step recipes for connecting HACI to your tools

---

## Table of Contents

1. [Monitoring & Observability](#monitoring--observability)
   - [Datadog](#datadog)
   - [New Relic](#new-relic)
   - [Prometheus & Grafana](#prometheus--grafana)
2. [Ticketing & Incident Management](#ticketing--incident-management)
   - [PagerDuty](#pagerduty)
   - [Jira](#jira)
   - [ServiceNow](#servicenow)
3. [Communication](#communication)
   - [Slack](#slack)
   - [Microsoft Teams](#microsoft-teams)
4. [Cloud Providers](#cloud-providers)
   - [AWS](#aws)
   - [Google Cloud Platform](#google-cloud-platform)
   - [Azure](#azure)
5. [Code & Version Control](#code--version-control)
   - [GitHub](#github)
   - [GitLab](#gitlab)
6. [Databases](#databases)
   - [PostgreSQL](#postgresql)
   - [MongoDB](#mongodb)

---

## Monitoring & Observability

### Datadog

**Integration Type:** MCP Server (recommended) or Direct API  
**Time to Complete:** 30 minutes  
**Capabilities Enabled:** Log search, metrics queries, APM traces, monitors

#### Prerequisites

- Datadog account with API access
- Admin or standard user role
- HACI deployment running

#### Step 1: Create Datadog API Keys

1. Log in to Datadog: https://app.datadoghq.com
2. Navigate to **Organization Settings → API Keys**
3. Click **+ New Key**
4. Name it: `HACI Integration`
5. Copy the API key (shown only once)

6. Navigate to **Organization Settings → Application Keys**
7. Click **+ New Key**
8. Name it: `HACI Integration`
9. Copy the application key

#### Step 2: Configure HACI Integration

**Option A: MCP Server (Recommended)**

```yaml
# config/integrations/datadog.yaml
integration:
  name: datadog
  type: mcp
  enabled: true
  
mcp:
  server_url: "https://mcp.datadoghq.com"
  
credentials:
  api_key: "${DATADOG_API_KEY}"        # From secret manager
  app_key: "${DATADOG_APP_KEY}"        # From secret manager
  
settings:
  site: "datadoghq.com"                # Or datadoghq.eu for EU
  default_timeframe: "1h"
  max_logs_per_query: 1000
```

**Option B: Direct API**

```yaml
# config/integrations/datadog.yaml
integration:
  name: datadog
  type: api
  enabled: true
  
api:
  base_url: "https://api.datadoghq.com/api/v2"
  
credentials:
  api_key: "${DATADOG_API_KEY}"
  app_key: "${DATADOG_APP_KEY}"
  
settings:
  site: "datadoghq.com"
  timeout_seconds: 30
  retry_attempts: 3
```

#### Step 3: Store Credentials

```bash
# Using AWS Secrets Manager
aws secretsmanager create-secret \
  --name haci/datadog \
  --secret-string '{"api_key":"YOUR_API_KEY","app_key":"YOUR_APP_KEY"}'

# Or using Kubernetes secrets
kubectl create secret generic haci-datadog \
  --from-literal=api_key=YOUR_API_KEY \
  --from-literal=app_key=YOUR_APP_KEY
```

#### Step 4: Test the Integration

```bash
# Via HACI CLI
haci integrations test datadog

# Expected output:
# ✅ Datadog connection successful
# ✅ Log search: OK (latency: 245ms)
# ✅ Metrics query: OK (latency: 189ms)
# ✅ APM traces: OK (latency: 312ms)
```

#### Step 5: Configure Agent Tools

```yaml
# config/agents/log_agent.yaml
tools:
  - name: datadog_search_logs
    integration: datadog
    description: "Search Datadog logs"
    parameters:
      query: string
      timeframe: string
      limit: integer
    
  - name: datadog_get_metrics
    integration: datadog
    description: "Query Datadog metrics"
    parameters:
      query: string
      from: timestamp
      to: timestamp
```

#### Verification

Create a test investigation:

```bash
curl -X POST "https://haci.yourcompany.com/api/v1/investigations" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Test Datadog Integration",
    "description": "Verify HACI can search Datadog logs",
    "severity": "low"
  }'
```

Watch the investigation use Datadog tools in the timeline.

#### Troubleshooting

| Issue | Solution |
|-------|----------|
| "403 Forbidden" | Verify API key has correct scopes |
| "No data returned" | Check timeframe and query syntax |
| Slow queries | Reduce `max_logs_per_query` |
| EU data not found | Set `site: datadoghq.eu` |

---

### New Relic

**Integration Type:** Direct API  
**Time to Complete:** 30 minutes  
**Capabilities Enabled:** Log search, NRQL queries, APM data, alerts

#### Prerequisites

- New Relic account (Pro or Enterprise)
- User API key
- Account ID

#### Step 1: Get New Relic Credentials

1. Log in to New Relic One
2. Click your name → **API Keys**
3. Click **Create a key**
4. Select **User** key type
5. Name it: `HACI Integration`
6. Copy the key

7. Note your **Account ID** from the URL or account settings

#### Step 2: Configure HACI Integration

```yaml
# config/integrations/newrelic.yaml
integration:
  name: newrelic
  type: api
  enabled: true
  
api:
  graphql_url: "https://api.newrelic.com/graphql"
  rest_url: "https://api.newrelic.com/v2"
  
credentials:
  api_key: "${NEWRELIC_API_KEY}"
  account_id: "${NEWRELIC_ACCOUNT_ID}"
  
settings:
  timeout_seconds: 30
  default_timeframe: "1 HOUR AGO"
```

#### Step 3: Configure Agent Tools

```yaml
# config/agents/log_agent.yaml
tools:
  - name: newrelic_nrql_query
    integration: newrelic
    description: "Execute NRQL query"
    parameters:
      nrql: string
      
  - name: newrelic_search_logs
    integration: newrelic
    description: "Search New Relic logs"
    parameters:
      query: string
      timeframe: string
```

#### Step 4: Test the Integration

```bash
haci integrations test newrelic

# Test NRQL query
haci tools test newrelic_nrql_query \
  --nrql "SELECT count(*) FROM Transaction SINCE 1 hour ago"
```

---

### Prometheus & Grafana

**Integration Type:** Direct API  
**Time to Complete:** 45 minutes  
**Capabilities Enabled:** Metrics queries, alert status, dashboard data

#### Step 1: Configure Prometheus Access

```yaml
# config/integrations/prometheus.yaml
integration:
  name: prometheus
  type: api
  enabled: true
  
api:
  base_url: "http://prometheus.monitoring.svc:9090"
  
credentials:
  # If authentication required
  bearer_token: "${PROMETHEUS_TOKEN}"
  
settings:
  timeout_seconds: 30
  default_range: "1h"
```

#### Step 2: Configure Grafana Access

```yaml
# config/integrations/grafana.yaml
integration:
  name: grafana
  type: api
  enabled: true
  
api:
  base_url: "https://grafana.yourcompany.com"
  
credentials:
  api_key: "${GRAFANA_API_KEY}"
  
settings:
  org_id: 1
```

#### Step 3: Create Grafana API Key

1. Log in to Grafana
2. Navigate to **Configuration → API Keys**
3. Click **Add API key**
4. Name: `HACI Integration`
5. Role: `Viewer`
6. Copy the key

#### Step 4: Configure Agent Tools

```yaml
tools:
  - name: prometheus_query
    integration: prometheus
    description: "Execute PromQL query"
    parameters:
      query: string
      time: timestamp
      
  - name: prometheus_query_range
    integration: prometheus
    description: "Execute PromQL range query"
    parameters:
      query: string
      start: timestamp
      end: timestamp
      step: string
      
  - name: grafana_get_dashboard
    integration: grafana
    description: "Get Grafana dashboard data"
    parameters:
      dashboard_uid: string
```

---

## Ticketing & Incident Management

### PagerDuty

**Integration Type:** MCP Server or Direct API  
**Time to Complete:** 30 minutes  
**Capabilities Enabled:** Incident creation, status updates, on-call lookup, alert correlation

#### Step 1: Create PagerDuty API Token

1. Log in to PagerDuty
2. Navigate to **Integrations → API Access Keys**
3. Click **Create New API Key**
4. Description: `HACI Integration`
5. Select **Read/Write** access
6. Copy the key

#### Step 2: Get Service IDs

Note the service IDs HACI should interact with:

1. Go to **Services → Service Directory**
2. Click each relevant service
3. Copy the **Service ID** from the URL

#### Step 3: Configure HACI Integration

```yaml
# config/integrations/pagerduty.yaml
integration:
  name: pagerduty
  type: api
  enabled: true
  
api:
  base_url: "https://api.pagerduty.com"
  
credentials:
  api_token: "${PAGERDUTY_API_TOKEN}"
  
settings:
  default_from_email: "haci@yourcompany.com"
  services:
    - id: "PXXXXXX"
      name: "Production API"
    - id: "PYYYYYY"
      name: "Database"
```

#### Step 4: Configure Webhook (Inbound)

To trigger HACI from PagerDuty incidents:

1. Go to **Services → [Your Service] → Integrations**
2. Click **Add Integration**
3. Select **Generic Webhook (V3)**
4. Set webhook URL: `https://haci.yourcompany.com/webhooks/pagerduty`
5. Select events: `incident.triggered`, `incident.acknowledged`

#### Step 5: Configure Agent Tools

```yaml
tools:
  - name: pagerduty_get_incident
    integration: pagerduty
    description: "Get PagerDuty incident details"
    parameters:
      incident_id: string
      
  - name: pagerduty_add_note
    integration: pagerduty
    description: "Add note to incident"
    parameters:
      incident_id: string
      note: string
      
  - name: pagerduty_get_oncall
    integration: pagerduty
    description: "Get current on-call"
    parameters:
      schedule_id: string
```

#### Step 6: Test the Integration

```bash
haci integrations test pagerduty

# Test getting on-call
haci tools test pagerduty_get_oncall --schedule_id PXXXXXX
```

---

### Jira

**Integration Type:** MCP Server or Direct API  
**Time to Complete:** 30 minutes  
**Capabilities Enabled:** Issue creation, updates, comments, transitions, search

#### Step 1: Create Jira API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click **Create API token**
3. Label: `HACI Integration`
4. Copy the token

#### Step 2: Configure HACI Integration

```yaml
# config/integrations/jira.yaml
integration:
  name: jira
  type: api
  enabled: true
  
api:
  base_url: "https://yourcompany.atlassian.net"
  
credentials:
  email: "haci-service@yourcompany.com"
  api_token: "${JIRA_API_TOKEN}"
  
settings:
  default_project: "OPS"
  default_issue_type: "Bug"
  custom_fields:
    severity: "customfield_10001"
    root_cause: "customfield_10002"
```

#### Step 3: Configure Project Permissions

Ensure the HACI service account has:
- Browse Project
- Create Issues
- Edit Issues
- Add Comments
- Transition Issues

#### Step 4: Configure Agent Tools

```yaml
tools:
  - name: jira_search
    integration: jira
    description: "Search Jira issues with JQL"
    parameters:
      jql: string
      max_results: integer
      
  - name: jira_create_issue
    integration: jira
    description: "Create Jira issue"
    parameters:
      project: string
      summary: string
      description: string
      issue_type: string
      
  - name: jira_add_comment
    integration: jira
    description: "Add comment to issue"
    parameters:
      issue_key: string
      comment: string
      
  - name: jira_transition
    integration: jira
    description: "Transition issue status"
    parameters:
      issue_key: string
      transition_name: string
```

#### Step 5: Set Up Webhook (Inbound)

To trigger HACI from Jira issues:

1. Go to **Settings → System → WebHooks**
2. Click **Create WebHook**
3. URL: `https://haci.yourcompany.com/webhooks/jira`
4. Events: Issue created, Issue updated
5. JQL filter: `project = OPS AND type = Bug`

---

### ServiceNow

**Integration Type:** Direct API  
**Time to Complete:** 45 minutes  
**Capabilities Enabled:** Incident management, CMDB queries, change requests

#### Step 1: Create ServiceNow Integration User

1. Log in to ServiceNow as admin
2. Navigate to **User Administration → Users**
3. Create new user: `haci_integration`
4. Assign roles:
   - `itil`
   - `rest_api_explorer`
   - `personalize_dictionary`

#### Step 2: Configure OAuth (Recommended)

1. Navigate to **System OAuth → Application Registry**
2. Click **New → Create OAuth API endpoint**
3. Name: `HACI Integration`
4. Note the Client ID and Client Secret

#### Step 3: Configure HACI Integration

```yaml
# config/integrations/servicenow.yaml
integration:
  name: servicenow
  type: api
  enabled: true
  
api:
  base_url: "https://yourcompany.service-now.com"
  
credentials:
  auth_type: oauth
  client_id: "${SNOW_CLIENT_ID}"
  client_secret: "${SNOW_CLIENT_SECRET}"
  username: "${SNOW_USERNAME}"
  password: "${SNOW_PASSWORD}"
  
settings:
  default_assignment_group: "DevOps"
  incident_table: "incident"
```

#### Step 4: Configure Agent Tools

```yaml
tools:
  - name: snow_get_incident
    integration: servicenow
    description: "Get ServiceNow incident"
    parameters:
      number: string
      
  - name: snow_create_incident
    integration: servicenow
    description: "Create ServiceNow incident"
    parameters:
      short_description: string
      description: string
      urgency: integer
      impact: integer
      
  - name: snow_query_cmdb
    integration: servicenow
    description: "Query CMDB"
    parameters:
      table: string
      query: string
```

---

## Communication

### Slack

**Integration Type:** Slack App  
**Time to Complete:** 30 minutes  
**Capabilities Enabled:** Notifications, approvals, status updates, interactive messages

#### Step 1: Create Slack App

1. Go to https://api.slack.com/apps
2. Click **Create New App**
3. Select **From scratch**
4. Name: `HACI`
5. Select your workspace

#### Step 2: Configure Bot Permissions

1. Go to **OAuth & Permissions**
2. Add Bot Token Scopes:
   - `chat:write`
   - `chat:write.public`
   - `channels:read`
   - `groups:read`
   - `im:write`
   - `users:read`
   - `users:read.email`

#### Step 3: Enable Interactive Components

1. Go to **Interactivity & Shortcuts**
2. Toggle **Interactivity** on
3. Set Request URL: `https://haci.yourcompany.com/webhooks/slack/interactive`

#### Step 4: Install App

1. Go to **Install App**
2. Click **Install to Workspace**
3. Authorize the permissions
4. Copy the **Bot User OAuth Token**

#### Step 5: Configure HACI Integration

```yaml
# config/integrations/slack.yaml
integration:
  name: slack
  type: app
  enabled: true
  
credentials:
  bot_token: "${SLACK_BOT_TOKEN}"
  signing_secret: "${SLACK_SIGNING_SECRET}"
  
settings:
  default_channel: "#ops-alerts"
  approval_channel: "#haci-approvals"
  notification_channel: "#haci-notifications"
```

#### Step 6: Invite Bot to Channels

```
/invite @HACI
```

Run this in each channel HACI should access.

#### Step 7: Configure Notification Templates

```yaml
# config/notifications/slack_templates.yaml
templates:
  approval_required:
    blocks:
      - type: header
        text: "🔔 HACI Approval Required"
      - type: section
        text: "*Ticket:* {{ticket_id}}\n*Finding:* {{finding}}\n*Confidence:* {{confidence}}%"
      - type: actions
        elements:
          - type: button
            text: "✅ Approve"
            action_id: "approve_{{approval_id}}"
            style: "primary"
          - type: button
            text: "❌ Reject"
            action_id: "reject_{{approval_id}}"
            style: "danger"
```

---

### Microsoft Teams

**Integration Type:** Teams App + Webhooks  
**Time to Complete:** 45 minutes  
**Capabilities Enabled:** Notifications, approvals, status updates

#### Step 1: Create Teams Incoming Webhook

1. Open Microsoft Teams
2. Go to the target channel
3. Click **...** → **Connectors**
4. Find **Incoming Webhook** → **Configure**
5. Name: `HACI Notifications`
6. Copy the webhook URL

#### Step 2: Create Azure Bot (for interactive)

For interactive approvals:

1. Go to Azure Portal → **Bot Services**
2. Click **Create**
3. Fill in bot details
4. Note the **App ID** and create a **Client Secret**

#### Step 3: Configure HACI Integration

```yaml
# config/integrations/teams.yaml
integration:
  name: teams
  type: webhook
  enabled: true
  
webhooks:
  notifications: "${TEAMS_WEBHOOK_URL}"
  
# For interactive bot (optional)
bot:
  app_id: "${TEAMS_BOT_APP_ID}"
  client_secret: "${TEAMS_BOT_SECRET}"
  tenant_id: "${TEAMS_TENANT_ID}"
```

#### Step 4: Configure Adaptive Cards

```yaml
# config/notifications/teams_templates.yaml
templates:
  approval_required:
    type: "AdaptiveCard"
    version: "1.4"
    body:
      - type: "TextBlock"
        text: "🔔 HACI Approval Required"
        weight: "bolder"
        size: "large"
      - type: "FactSet"
        facts:
          - title: "Ticket"
            value: "{{ticket_id}}"
          - title: "Finding"
            value: "{{finding}}"
          - title: "Confidence"
            value: "{{confidence}}%"
    actions:
      - type: "Action.Submit"
        title: "✅ Approve"
        data:
          action: "approve"
          approval_id: "{{approval_id}}"
```

---

## Cloud Providers

### AWS

**Integration Type:** Direct API (boto3)  
**Time to Complete:** 45 minutes  
**Capabilities Enabled:** CloudWatch logs/metrics, EC2, RDS, ECS, Lambda, S3

#### Step 1: Create IAM Role for HACI

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams",
        "logs:GetLogEvents",
        "logs:FilterLogEvents",
        "cloudwatch:GetMetricData",
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:ListMetrics",
        "ec2:DescribeInstances",
        "ec2:DescribeInstanceStatus",
        "rds:DescribeDBInstances",
        "rds:DescribeDBClusters",
        "ecs:DescribeServices",
        "ecs:DescribeTasks",
        "ecs:ListTasks",
        "lambda:GetFunction",
        "lambda:ListFunctions"
      ],
      "Resource": "*"
    }
  ]
}
```

#### Step 2: Configure Access

**Option A: IAM Role (EKS)**

If running on EKS, use IAM Roles for Service Accounts:

```yaml
# k8s/haci-serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: haci
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789:role/haci-role
```

**Option B: Access Keys**

```yaml
# config/integrations/aws.yaml
integration:
  name: aws
  type: sdk
  enabled: true
  
credentials:
  access_key_id: "${AWS_ACCESS_KEY_ID}"
  secret_access_key: "${AWS_SECRET_ACCESS_KEY}"
  
settings:
  default_region: "us-east-1"
  regions:
    - us-east-1
    - us-west-2
    - eu-west-1
```

#### Step 3: Configure Agent Tools

```yaml
tools:
  - name: aws_cloudwatch_logs
    integration: aws
    description: "Search CloudWatch logs"
    parameters:
      log_group: string
      filter_pattern: string
      start_time: timestamp
      end_time: timestamp
      
  - name: aws_cloudwatch_metrics
    integration: aws
    description: "Get CloudWatch metrics"
    parameters:
      namespace: string
      metric_name: string
      dimensions: object
      
  - name: aws_describe_ec2
    integration: aws
    description: "Describe EC2 instances"
    parameters:
      instance_ids: array
      filters: object
      
  - name: aws_describe_rds
    integration: aws
    description: "Describe RDS instances"
    parameters:
      db_instance_identifier: string
```

---

### Google Cloud Platform

**Integration Type:** Direct API  
**Time to Complete:** 45 minutes  
**Capabilities Enabled:** Cloud Logging, Monitoring, Compute, Cloud SQL, GKE

#### Step 1: Create Service Account

```bash
# Create service account
gcloud iam service-accounts create haci-integration \
  --display-name="HACI Integration"

# Grant roles
gcloud projects add-iam-policy-binding YOUR_PROJECT \
  --member="serviceAccount:haci-integration@YOUR_PROJECT.iam.gserviceaccount.com" \
  --role="roles/logging.viewer"

gcloud projects add-iam-policy-binding YOUR_PROJECT \
  --member="serviceAccount:haci-integration@YOUR_PROJECT.iam.gserviceaccount.com" \
  --role="roles/monitoring.viewer"

gcloud projects add-iam-policy-binding YOUR_PROJECT \
  --member="serviceAccount:haci-integration@YOUR_PROJECT.iam.gserviceaccount.com" \
  --role="roles/compute.viewer"

# Create key
gcloud iam service-accounts keys create haci-gcp-key.json \
  --iam-account=haci-integration@YOUR_PROJECT.iam.gserviceaccount.com
```

#### Step 2: Configure HACI Integration

```yaml
# config/integrations/gcp.yaml
integration:
  name: gcp
  type: sdk
  enabled: true
  
credentials:
  # Path to service account key or use workload identity
  service_account_key: "${GCP_SERVICE_ACCOUNT_KEY}"
  
settings:
  default_project: "your-project-id"
  projects:
    - your-project-id
    - your-other-project
```

#### Step 3: Configure Agent Tools

```yaml
tools:
  - name: gcp_logging_search
    integration: gcp
    description: "Search Cloud Logging"
    parameters:
      filter: string
      project: string
      
  - name: gcp_monitoring_query
    integration: gcp
    description: "Query Cloud Monitoring metrics"
    parameters:
      filter: string
      interval_start: timestamp
      interval_end: timestamp
```

---

### Azure

**Integration Type:** Direct API  
**Time to Complete:** 45 minutes  
**Capabilities Enabled:** Monitor logs, metrics, VMs, SQL Database, AKS

#### Step 1: Create App Registration

1. Go to Azure Portal → **Azure Active Directory**
2. Navigate to **App registrations → New registration**
3. Name: `HACI Integration`
4. Register

5. Go to **Certificates & secrets**
6. Create new client secret
7. Copy the secret value

8. Note the **Application (client) ID** and **Directory (tenant) ID**

#### Step 2: Assign Permissions

```bash
# Assign Reader role at subscription level
az role assignment create \
  --assignee APP_ID \
  --role "Reader" \
  --scope /subscriptions/YOUR_SUBSCRIPTION_ID

# Assign Log Analytics Reader
az role assignment create \
  --assignee APP_ID \
  --role "Log Analytics Reader" \
  --scope /subscriptions/YOUR_SUBSCRIPTION_ID
```

#### Step 3: Configure HACI Integration

```yaml
# config/integrations/azure.yaml
integration:
  name: azure
  type: sdk
  enabled: true
  
credentials:
  tenant_id: "${AZURE_TENANT_ID}"
  client_id: "${AZURE_CLIENT_ID}"
  client_secret: "${AZURE_CLIENT_SECRET}"
  subscription_id: "${AZURE_SUBSCRIPTION_ID}"
  
settings:
  log_analytics_workspace_id: "YOUR_WORKSPACE_ID"
```

---

## Code & Version Control

### GitHub

**Integration Type:** MCP Server or Direct API  
**Time to Complete:** 20 minutes  
**Capabilities Enabled:** Code search, PR/commit history, deployment status, actions

#### Step 1: Create GitHub App or PAT

**Option A: Personal Access Token (Simple)**

1. Go to GitHub → **Settings → Developer settings → Personal access tokens**
2. Click **Generate new token (classic)**
3. Select scopes:
   - `repo` (for private repos)
   - `read:org`
4. Copy the token

**Option B: GitHub App (Recommended for org)**

1. Go to **Organization Settings → Developer settings → GitHub Apps**
2. Create new app with permissions:
   - Repository: Contents (Read), Pull requests (Read), Actions (Read)
3. Install on repositories

#### Step 2: Configure HACI Integration

```yaml
# config/integrations/github.yaml
integration:
  name: github
  type: api
  enabled: true
  
api:
  base_url: "https://api.github.com"
  
credentials:
  # For PAT
  token: "${GITHUB_TOKEN}"
  
  # For GitHub App
  # app_id: "${GITHUB_APP_ID}"
  # private_key: "${GITHUB_PRIVATE_KEY}"
  # installation_id: "${GITHUB_INSTALLATION_ID}"
  
settings:
  organization: "your-org"
  default_repos:
    - your-org/main-service
    - your-org/api-gateway
```

#### Step 3: Configure Agent Tools

```yaml
tools:
  - name: github_search_code
    integration: github
    description: "Search code in repositories"
    parameters:
      query: string
      repo: string
      
  - name: github_get_commits
    integration: github
    description: "Get recent commits"
    parameters:
      repo: string
      since: timestamp
      path: string
      
  - name: github_get_deployments
    integration: github
    description: "Get deployment history"
    parameters:
      repo: string
      environment: string
```

---

### GitLab

**Integration Type:** Direct API  
**Time to Complete:** 20 minutes  
**Capabilities Enabled:** Code search, MR history, pipelines, deployments

#### Step 1: Create GitLab Access Token

1. Go to GitLab → **User Settings → Access Tokens**
2. Name: `HACI Integration`
3. Select scopes: `read_api`, `read_repository`
4. Create and copy token

#### Step 2: Configure HACI Integration

```yaml
# config/integrations/gitlab.yaml
integration:
  name: gitlab
  type: api
  enabled: true
  
api:
  base_url: "https://gitlab.com/api/v4"  # Or your self-hosted URL
  
credentials:
  token: "${GITLAB_TOKEN}"
  
settings:
  default_group: "your-group"
```

---

## Databases

### PostgreSQL

**Integration Type:** Direct Connection  
**Time to Complete:** 30 minutes  
**Capabilities Enabled:** Query analysis, connection stats, table sizes, slow queries

#### Step 1: Create Database User

```sql
-- Create read-only user for HACI
CREATE USER haci_readonly WITH PASSWORD 'secure_password';

-- Grant minimal permissions
GRANT CONNECT ON DATABASE your_database TO haci_readonly;
GRANT USAGE ON SCHEMA public TO haci_readonly;
GRANT SELECT ON pg_stat_activity TO haci_readonly;
GRANT SELECT ON pg_stat_statements TO haci_readonly;
GRANT SELECT ON pg_locks TO haci_readonly;

-- For table metadata
GRANT SELECT ON information_schema.tables TO haci_readonly;
GRANT SELECT ON information_schema.columns TO haci_readonly;
```

#### Step 2: Enable pg_stat_statements

```sql
-- In postgresql.conf
shared_preload_libraries = 'pg_stat_statements'

-- Then create extension
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

#### Step 3: Configure HACI Integration

```yaml
# config/integrations/postgresql.yaml
integration:
  name: postgresql
  type: database
  enabled: true
  
connection:
  host: "${PG_HOST}"
  port: 5432
  database: "${PG_DATABASE}"
  
credentials:
  username: "${PG_USERNAME}"
  password: "${PG_PASSWORD}"
  ssl_mode: "require"
  
settings:
  connection_pool_size: 5
  query_timeout_seconds: 30
```

#### Step 4: Configure Agent Tools

```yaml
tools:
  - name: pg_slow_queries
    integration: postgresql
    description: "Get slow queries from pg_stat_statements"
    parameters:
      min_duration_ms: integer
      limit: integer
      
  - name: pg_active_connections
    integration: postgresql
    description: "Get active database connections"
    parameters: {}
    
  - name: pg_locks
    integration: postgresql
    description: "Get current locks"
    parameters: {}
    
  - name: pg_table_sizes
    integration: postgresql
    description: "Get table sizes"
    parameters:
      schema: string
```

---

### MongoDB

**Integration Type:** Direct Connection  
**Time to Complete:** 30 minutes  
**Capabilities Enabled:** Query profiling, collection stats, replication status

#### Step 1: Create Database User

```javascript
db.createUser({
  user: "haci_readonly",
  pwd: "secure_password",
  roles: [
    { role: "read", db: "your_database" },
    { role: "clusterMonitor", db: "admin" }
  ]
});
```

#### Step 2: Enable Profiling

```javascript
// Enable profiling for slow queries (>100ms)
db.setProfilingLevel(1, { slowms: 100 });
```

#### Step 3: Configure HACI Integration

```yaml
# config/integrations/mongodb.yaml
integration:
  name: mongodb
  type: database
  enabled: true
  
connection:
  uri: "${MONGODB_URI}"
  # Or individual settings:
  # host: "${MONGO_HOST}"
  # port: 27017
  # replica_set: "rs0"
  
credentials:
  username: "${MONGO_USERNAME}"
  password: "${MONGO_PASSWORD}"
  auth_database: "admin"
  
settings:
  default_database: "your_database"
  connection_pool_size: 5
```

#### Step 4: Configure Agent Tools

```yaml
tools:
  - name: mongo_profiler
    integration: mongodb
    description: "Get slow operations from profiler"
    parameters:
      database: string
      min_duration_ms: integer
      
  - name: mongo_collection_stats
    integration: mongodb
    description: "Get collection statistics"
    parameters:
      database: string
      collection: string
      
  - name: mongo_repl_status
    integration: mongodb
    description: "Get replica set status"
    parameters: {}
```

---

## Integration Health Monitoring

### Setting Up Health Checks

```yaml
# config/health_checks.yaml
health_checks:
  interval_seconds: 60
  
  integrations:
    datadog:
      check: api_ping
      timeout: 5s
      alert_threshold: 3  # failures before alert
      
    pagerduty:
      check: api_ping
      timeout: 5s
      
    aws:
      check: sts_get_caller_identity
      timeout: 10s
```

### Viewing Integration Health

```bash
# CLI
haci integrations health

# Output:
# Integration      Status    Latency    Last Check
# ─────────────────────────────────────────────────
# datadog          ✅ OK     245ms      2 min ago
# pagerduty        ✅ OK     189ms      2 min ago
# aws              ✅ OK     312ms      2 min ago
# slack            ⚠️ SLOW   1.2s       2 min ago
# postgresql       ✅ OK     45ms       2 min ago
```

### Alerting on Integration Failures

```yaml
# config/alerts.yaml
alerts:
  integration_failure:
    condition: "integration.status == 'unhealthy'"
    channels:
      - slack: "#ops-alerts"
      - pagerduty: "PXXXXXX"
    message: "HACI integration {{integration.name}} is unhealthy: {{integration.error}}"
```

---

## Next Steps

After completing integrations:

1. **Test each integration** using `haci integrations test <name>`
2. **Configure agents** to use the new tools
3. **Run a test investigation** to verify end-to-end flow
4. **Set up monitoring** for integration health
5. **Document any custom configurations** for your team

---

## Getting Help

- **Integration issues:** Check the [Troubleshooting Guide](./HACI_Troubleshooting_Guide.md)
- **API documentation:** Refer to [API Reference](./HACI_API_Reference.md)
- **Support:** Contact haci-support@yourcompany.com

---

*Last updated: January 2026 | Version 1.0*
