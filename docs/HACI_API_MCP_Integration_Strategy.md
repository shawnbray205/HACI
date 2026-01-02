# HACI: API and MCP Integration Strategy
## Comprehensive Technical Documentation for External System Connectivity

**Document ID:** HACI-API-MCP-001  
**Version:** 1.0  
**Date:** December 2025  
**Classification:** Technical Architecture & Implementation Guide

---

## Executive Summary

This document defines HACI's comprehensive strategy for integrating with external systems through both traditional REST/GraphQL APIs and the Model Context Protocol (MCP). As an enterprise-grade AI automation platform, HACI requires robust, scalable, and standardized approaches to connect with ticketing systems, monitoring platforms, cloud infrastructure, databases, and collaboration tools.

**Key Strategic Decisions:**

1. **Hybrid Integration Architecture** — Leverage both traditional APIs and MCP based on use case requirements
2. **MCP-First for New Integrations** — Adopt MCP as the preferred standard for new tool integrations
3. **Provider Abstraction Layer** — Maintain vendor-agnostic interfaces regardless of integration method
4. **Progressive Migration** — Transition existing API integrations to MCP where beneficial

---

## Table of Contents

1. [Integration Architecture Overview](#1-integration-architecture-overview)
2. [Traditional API Integration Strategy](#2-traditional-api-integration-strategy)
3. [Model Context Protocol (MCP) Strategy](#3-model-context-protocol-mcp-strategy)
4. [API vs MCP Decision Framework](#4-api-vs-mcp-decision-framework)
5. [HACI MCP Server Architecture](#5-haci-mcp-server-architecture)
6. [HACI MCP Client Implementation](#6-haci-mcp-client-implementation)
7. [Integration Patterns by Domain](#7-integration-patterns-by-domain)
8. [Security and Authentication](#8-security-and-authentication)
9. [Performance and Optimization](#9-performance-and-optimization)
10. [Implementation Roadmap](#10-implementation-roadmap)
11. [Appendices](#11-appendices)

---

## 1. Integration Architecture Overview

### 1.1 The Integration Challenge

HACI operates as an intelligent orchestration layer that must seamlessly interact with:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    HACI EXTERNAL INTEGRATION LANDSCAPE                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  TICKETING               MONITORING             CLOUD                       │
│  ┌──────────┐           ┌──────────┐           ┌──────────┐                │
│  │  Jira    │           │ Datadog  │           │   AWS    │                │
│  │ServiceNow│           │ New Relic│           │  Azure   │                │
│  │PagerDuty │           │ Splunk   │           │   GCP    │                │
│  └──────────┘           │Prometheus│           │   K8s    │                │
│                         └──────────┘           └──────────┘                │
│                                                                             │
│  CODE/CI-CD              DATABASES              COLLABORATION              │
│  ┌──────────┐           ┌──────────┐           ┌──────────┐                │
│  │  GitHub  │           │PostgreSQL│           │  Slack   │                │
│  │  GitLab  │           │  MySQL   │           │  Teams   │                │
│  │ Jenkins  │           │ MongoDB  │           │Confluence│                │
│  │ CircleCI │           │  Redis   │           │  Notion  │                │
│  └──────────┘           └──────────┘           └──────────┘                │
│                                                                             │
│  SECURITY                LLM PROVIDERS          INTERNAL SYSTEMS           │
│  ┌──────────┐           ┌──────────┐           ┌──────────┐                │
│  │  Vault   │           │Anthropic │           │  CMDB    │                │
│  │  Snyk    │           │  OpenAI  │           │ Runbooks │                │
│  │  Okta    │           │  Google  │           │    KB    │                │
│  └──────────┘           └──────────┘           └──────────┘                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Dual Integration Strategy

HACI employs a **hybrid integration architecture** that leverages both traditional APIs and MCP:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     HACI DUAL INTEGRATION ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                           ┌─────────────────┐                               │
│                           │  HACI CORE      │                               │
│                           │  ORCHESTRATOR   │                               │
│                           └────────┬────────┘                               │
│                                    │                                        │
│                    ┌───────────────┼───────────────┐                        │
│                    │               │               │                        │
│                    ▼               ▼               ▼                        │
│           ┌──────────────┐ ┌─────────────┐ ┌──────────────┐                │
│           │    AGENT     │ │   AGENT     │ │    AGENT     │                │
│           │  (Log Agent) │ │(Code Agent) │ │ (DB Agent)   │                │
│           └──────┬───────┘ └──────┬──────┘ └──────┬───────┘                │
│                  │                │               │                        │
│                  ▼                ▼               ▼                        │
│        ┌─────────────────────────────────────────────────────┐             │
│        │           UNIFIED INTEGRATION LAYER                  │             │
│        │  ┌─────────────────────┬─────────────────────────┐  │             │
│        │  │   API ADAPTER       │    MCP CLIENT           │  │             │
│        │  │   FRAMEWORK         │    FRAMEWORK            │  │             │
│        │  │                     │                         │  │             │
│        │  │  • REST Clients     │  • MCP Client Manager   │  │             │
│        │  │  • GraphQL Clients  │  • Tool Discovery       │  │             │
│        │  │  • gRPC Clients     │  • Resource Access      │  │             │
│        │  │  • WebSocket Mgr    │  • Prompt Templates     │  │             │
│        │  │  • Rate Limiters    │  • Sampling Interface   │  │             │
│        │  │  • Circuit Breakers │  • Notification Handler │  │             │
│        │  └─────────────────────┴─────────────────────────┘  │             │
│        └─────────────────────────────────────────────────────┘             │
│                                    │                                        │
│           ┌────────────────────────┼────────────────────────┐              │
│           │                        │                        │              │
│           ▼                        ▼                        ▼              │
│    ┌─────────────┐         ┌─────────────┐         ┌─────────────┐        │
│    │ TRADITIONAL │         │    MCP      │         │   HYBRID    │        │
│    │    APIs     │         │  SERVERS    │         │  (Both)     │        │
│    ├─────────────┤         ├─────────────┤         ├─────────────┤        │
│    │• Jira REST  │         │• GitHub MCP │         │• Datadog    │        │
│    │• AWS APIs   │         │• Slack MCP  │         │  (API +     │        │
│    │• PostgreSQL │         │• GDrive MCP │         │   MCP)      │        │
│    │  Direct     │         │• Postgres   │         │• Kubernetes │        │
│    │• Datadog API│         │  MCP        │         │             │        │
│    └─────────────┘         └─────────────┘         └─────────────┘        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.3 Integration Philosophy

**Core Principles:**

| Principle | Description | Implementation |
|-----------|-------------|----------------|
| **Abstraction** | Vendors are interchangeable | Unified interface layer |
| **Resilience** | No single points of failure | Multi-provider fallbacks |
| **Efficiency** | Minimize token usage | MCP code execution patterns |
| **Security** | Zero trust architecture | Credential isolation per integration |
| **Observability** | Full audit trails | Log all API/MCP interactions |

---

## 2. Traditional API Integration Strategy

### 2.1 Current API Integration Architecture

HACI's existing API integration follows a structured abstraction pattern:

```python
# Abstract Integration Interface
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass

@dataclass
class IntegrationResponse:
    """Standardized response from any integration"""
    success: bool
    data: Optional[Dict[str, Any]]
    error: Optional[str]
    metadata: Dict[str, Any]

class BaseIntegration(ABC):
    """Abstract base class for all integrations"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._setup_client()
    
    @abstractmethod
    async def _setup_client(self) -> None:
        """Initialize the vendor-specific client"""
        pass
    
    @abstractmethod
    async def execute(
        self, 
        operation: str, 
        params: Dict[str, Any]
    ) -> IntegrationResponse:
        """Execute an operation against the vendor API"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Verify the integration is operational"""
        pass


# Concrete Implementation Example: Jira
class JiraIntegration(BaseIntegration):
    """Jira REST API integration"""
    
    async def _setup_client(self) -> None:
        self.base_url = self.config["base_url"]
        self.auth = (
            self.config["username"], 
            self.config["api_token"]
        )
        self.session = aiohttp.ClientSession()
    
    async def execute(
        self, 
        operation: str, 
        params: Dict[str, Any]
    ) -> IntegrationResponse:
        operations = {
            "get_issue": self._get_issue,
            "create_issue": self._create_issue,
            "update_issue": self._update_issue,
            "add_comment": self._add_comment,
            "search_jql": self._search_jql
        }
        
        if operation not in operations:
            return IntegrationResponse(
                success=False,
                data=None,
                error=f"Unknown operation: {operation}",
                metadata={}
            )
        
        return await operations[operation](params)
    
    @with_circuit_breaker(fail_max=5, timeout=60)
    @with_rate_limit(calls=150, period=1)
    async def _get_issue(self, params: Dict) -> IntegrationResponse:
        """Get a Jira issue by key"""
        issue_key = params["issue_key"]
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"
        
        async with self.session.get(url, auth=self.auth) as resp:
            if resp.status == 200:
                data = await resp.json()
                return IntegrationResponse(
                    success=True,
                    data=data,
                    error=None,
                    metadata={"status_code": resp.status}
                )
            else:
                return IntegrationResponse(
                    success=False,
                    data=None,
                    error=f"API error: {resp.status}",
                    metadata={"status_code": resp.status}
                )
```

### 2.2 API Integration Patterns

**Pattern 1: Direct REST API Calls**

```python
# Used for: Jira, ServiceNow, PagerDuty, Datadog
class RESTIntegration(BaseIntegration):
    """Standard REST API pattern"""
    
    async def execute(self, operation: str, params: Dict) -> IntegrationResponse:
        endpoint = self._build_endpoint(operation, params)
        method = self._get_method(operation)
        
        async with self.session.request(
            method=method,
            url=endpoint,
            json=params.get("body"),
            headers=self._get_headers()
        ) as response:
            return await self._process_response(response)
```

**Pattern 2: GraphQL API Integration**

```python
# Used for: GitHub, GitLab
class GraphQLIntegration(BaseIntegration):
    """GraphQL API pattern"""
    
    async def execute(self, operation: str, params: Dict) -> IntegrationResponse:
        query = self._get_query(operation)
        variables = params.get("variables", {})
        
        async with self.session.post(
            url=self.graphql_endpoint,
            json={"query": query, "variables": variables}
        ) as response:
            return await self._process_graphql_response(response)
```

**Pattern 3: Direct Database Connection**

```python
# Used for: PostgreSQL, MySQL, MongoDB
class DatabaseIntegration(BaseIntegration):
    """Direct database connection pattern"""
    
    async def _setup_client(self) -> None:
        self.pool = await asyncpg.create_pool(
            dsn=self.config["connection_string"],
            min_size=5,
            max_size=20
        )
    
    async def execute(self, operation: str, params: Dict) -> IntegrationResponse:
        query = params.get("query")
        args = params.get("args", [])
        
        async with self.pool.acquire() as conn:
            result = await conn.fetch(query, *args)
            return IntegrationResponse(
                success=True,
                data={"rows": [dict(r) for r in result]},
                error=None,
                metadata={"row_count": len(result)}
            )
```

### 2.3 API Rate Limiting and Resilience

```python
from pybreaker import CircuitBreaker
from ratelimit import limits, sleep_and_retry

class ResilientAPIClient:
    """API client with circuit breaker and rate limiting"""
    
    def __init__(self, vendor: str, config: Dict):
        self.vendor = vendor
        self.config = config
        
        # Configure circuit breaker per vendor
        self.circuit_breaker = CircuitBreaker(
            fail_max=config.get("fail_max", 5),
            timeout_duration=config.get("timeout", 60)
        )
        
        # Rate limits per vendor
        self.rate_limits = {
            "jira": {"calls": 150, "period": 1},
            "datadog": {"calls": 300, "period": 3600},
            "github": {"calls": 5000, "period": 3600},
            "pagerduty": {"calls": 960, "period": 60}
        }
    
    @sleep_and_retry
    def _rate_limited_call(self, func, *args, **kwargs):
        """Apply rate limiting based on vendor"""
        limits_config = self.rate_limits.get(self.vendor, {"calls": 100, "period": 60})
        
        @limits(calls=limits_config["calls"], period=limits_config["period"])
        def limited_func():
            return func(*args, **kwargs)
        
        return limited_func()
    
    async def call(self, func, *args, **kwargs):
        """Execute API call with resilience patterns"""
        try:
            return await self.circuit_breaker.call_async(
                self._rate_limited_call,
                func,
                *args,
                **kwargs
            )
        except CircuitBreakerError:
            # Fallback to alternative provider
            return await self._fallback_call(func, *args, **kwargs)
```

---

## 3. Model Context Protocol (MCP) Strategy

### 3.1 Why MCP for HACI?

The Model Context Protocol addresses several challenges that are particularly relevant to HACI:

**The N×M Integration Problem:**

```
                    WITHOUT MCP                          WITH MCP
                    
    ┌───────┐                                    ┌───────┐
    │Log    │──┬──Jira                          │Log    │
    │Agent  │  ├──Datadog                       │Agent  │──┐
    └───────┘  ├──GitHub                        └───────┘  │
               ├──Slack                                    │
    ┌───────┐  ├──AWS                           ┌───────┐  │
    │Code   │──┼──Jira                          │Code   │──┤
    │Agent  │  ├──Datadog                       │Agent  │  │
    └───────┘  ├──GitHub    N×M = 50            └───────┘  │    ┌─────────────┐
               ├──Slack     integrations                   │    │             │
    ┌───────┐  ├──AWS                           ┌───────┐  │    │  UNIFIED    │
    │Infra  │──┼──Jira                          │Infra  │──┼────│    MCP      │
    │Agent  │  ├──Datadog                       │Agent  │  │    │   LAYER     │
    └───────┘  ├──GitHub                        └───────┘  │    │             │
               ├──Slack                                    │    │  N+M = 15   │
    ┌───────┐  ├──AWS                           ┌───────┐  │    │integrations │
    │DB     │──┼──Jira                          │DB     │──┤    │             │
    │Agent  │  ├──Datadog                       │Agent  │  │    └──────┬──────┘
    └───────┘  └──GitHub...                     └───────┘  │           │
                                                           └───────────┼──MCP Servers
    10 agents × 5 vendors = 50 custom                                  ├──Jira MCP
    integrations to build & maintain                                   ├──Datadog MCP
                                                                       ├──GitHub MCP
                                                                       ├──Slack MCP
                                                                       └──AWS MCP
```

**Context Window Efficiency:**

MCP enables HACI to use **code execution patterns** that dramatically reduce token usage:

```
Traditional Approach (150,000+ tokens):
├── Load ALL tool definitions upfront
├── Include ALL in every LLM call
└── Results: Slow, expensive, context bloat

MCP Code Execution (2,000 tokens):
├── Agents write code to discover needed tools
├── Load ONLY relevant tool definitions
├── Execute logic in code, not prompts
└── Results: 98.7% token reduction
```

### 3.2 MCP Architecture in HACI

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        HACI MCP ARCHITECTURE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         MCP HOST (HACI CORE)                         │   │
│  │                                                                      │   │
│  │   ┌───────────────┐  ┌───────────────┐  ┌───────────────┐           │   │
│  │   │ Meta-         │  │ Swarm         │  │ Human         │           │   │
│  │   │ Orchestrator  │  │ Coordinator   │  │ Interface     │           │   │
│  │   └───────┬───────┘  └───────┬───────┘  └───────┬───────┘           │   │
│  │           │                  │                  │                    │   │
│  │           └──────────────────┼──────────────────┘                    │   │
│  │                              │                                       │   │
│  │                              ▼                                       │   │
│  │   ┌──────────────────────────────────────────────────────────────┐  │   │
│  │   │                    MCP CLIENT MANAGER                         │  │   │
│  │   │                                                               │  │   │
│  │   │  • Server Discovery & Registry                                │  │   │
│  │   │  • Connection Pool Management                                 │  │   │
│  │   │  • Tool/Resource/Prompt Routing                               │  │   │
│  │   │  • Sampling Request Handler                                   │  │   │
│  │   │  • Notification Dispatcher                                    │  │   │
│  │   │                                                               │  │   │
│  │   └──────────────────────────────────────────────────────────────┘  │   │
│  │                              │                                       │   │
│  └──────────────────────────────┼───────────────────────────────────────┘   │
│                                 │                                           │
│        ┌────────────────────────┼────────────────────────┐                  │
│        │                        │                        │                  │
│        ▼                        ▼                        ▼                  │
│  ┌───────────┐           ┌───────────┐           ┌───────────┐             │
│  │MCP CLIENT │           │MCP CLIENT │           │MCP CLIENT │             │
│  │(Ticketing)│           │(Monitoring│           │  (Code)   │             │
│  └─────┬─────┘           └─────┬─────┘           └─────┬─────┘             │
│        │                       │                       │                    │
│        │ JSON-RPC 2.0          │ JSON-RPC 2.0          │ JSON-RPC 2.0       │
│        │ (stdio/SSE/HTTP)      │ (stdio/SSE/HTTP)      │ (stdio/SSE/HTTP)   │
│        │                       │                       │                    │
│        ▼                       ▼                       ▼                    │
│  ┌───────────┐           ┌───────────┐           ┌───────────┐             │
│  │MCP SERVER │           │MCP SERVER │           │MCP SERVER │             │
│  │   Jira    │           │  Datadog  │           │  GitHub   │             │
│  │           │           │           │           │           │             │
│  │ PRIMITIVES│           │ PRIMITIVES│           │ PRIMITIVES│             │
│  │ • Tools   │           │ • Tools   │           │ • Tools   │             │
│  │ • Prompts │           │ • Resources│           │ • Resources│            │
│  │ • Resources│          │ • Prompts │           │ • Prompts │             │
│  └─────┬─────┘           └─────┬─────┘           └─────┬─────┘             │
│        │                       │                       │                    │
│        ▼                       ▼                       ▼                    │
│  ┌───────────┐           ┌───────────┐           ┌───────────┐             │
│  │ Jira API  │           │Datadog API│           │GitHub API │             │
│  └───────────┘           └───────────┘           └───────────┘             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.3 MCP Primitives for HACI

MCP defines three server-side primitives that HACI will leverage:

#### **Tools** — Executable Functions

```python
# Example: Jira MCP Server Tool Definitions

tools = [
    {
        "name": "jira.createIssue",
        "description": "Create a new Jira issue in a specified project",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project": {
                    "type": "string",
                    "description": "Project key (e.g., 'HACI')"
                },
                "issueType": {
                    "type": "string",
                    "enum": ["Bug", "Task", "Story", "Epic"],
                    "description": "Type of issue to create"
                },
                "summary": {
                    "type": "string",
                    "description": "Issue title/summary"
                },
                "description": {
                    "type": "string",
                    "description": "Detailed issue description"
                },
                "priority": {
                    "type": "string",
                    "enum": ["Highest", "High", "Medium", "Low", "Lowest"]
                }
            },
            "required": ["project", "issueType", "summary"]
        }
    },
    {
        "name": "jira.addComment",
        "description": "Add a comment to an existing Jira issue",
        "inputSchema": {
            "type": "object",
            "properties": {
                "issueKey": {"type": "string"},
                "comment": {"type": "string"}
            },
            "required": ["issueKey", "comment"]
        }
    },
    {
        "name": "jira.searchJQL",
        "description": "Search Jira issues using JQL query",
        "inputSchema": {
            "type": "object",
            "properties": {
                "jql": {
                    "type": "string",
                    "description": "JQL query string"
                },
                "maxResults": {
                    "type": "integer",
                    "default": 50
                }
            },
            "required": ["jql"]
        }
    }
]
```

#### **Resources** — Structured Data Sources

```python
# Example: Datadog MCP Server Resource Definitions

resources = [
    {
        "uri": "datadog://metrics/{query}",
        "name": "Datadog Metrics",
        "description": "Time series metrics data from Datadog",
        "mimeType": "application/json"
    },
    {
        "uri": "datadog://logs/{query}",
        "name": "Datadog Logs",
        "description": "Log entries matching query",
        "mimeType": "application/json"
    },
    {
        "uri": "datadog://apm/traces/{service}",
        "name": "APM Traces",
        "description": "Application performance traces",
        "mimeType": "application/json"
    }
]
```

#### **Prompts** — Instruction Templates

```python
# Example: GitHub MCP Server Prompt Templates

prompts = [
    {
        "name": "analyze_pr",
        "description": "Template for analyzing a pull request",
        "arguments": [
            {
                "name": "pr_number",
                "description": "Pull request number to analyze",
                "required": True
            },
            {
                "name": "focus_areas",
                "description": "Specific areas to focus on",
                "required": False
            }
        ]
    },
    {
        "name": "review_security",
        "description": "Security-focused code review template",
        "arguments": [
            {
                "name": "file_paths",
                "description": "Files to review",
                "required": True
            }
        ]
    }
]
```

### 3.4 MCP Communication Patterns

**Transport Mechanisms:**

| Transport | Use Case | HACI Implementation |
|-----------|----------|---------------------|
| **stdio** | Local MCP servers | Agent-local tools |
| **HTTP/SSE** | Remote MCP servers | Enterprise deployments |
| **WebSocket** | Bidirectional streaming | Real-time monitoring |

**Message Flow:**

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     MCP MESSAGE FLOW IN HACI                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  HACI Agent                    MCP Server                    External API    │
│      │                             │                              │          │
│      │  ──────────────────────────>│                              │          │
│      │    initialize               │                              │          │
│      │    {protocolVersion, ...}   │                              │          │
│      │                             │                              │          │
│      │  <──────────────────────────│                              │          │
│      │    initialized              │                              │          │
│      │    {capabilities, ...}      │                              │          │
│      │                             │                              │          │
│      │  ──────────────────────────>│                              │          │
│      │    tools/list               │                              │          │
│      │                             │                              │          │
│      │  <──────────────────────────│                              │          │
│      │    {tools: [...]}           │                              │          │
│      │                             │                              │          │
│      │  ──────────────────────────>│                              │          │
│      │    tools/call               │                              │          │
│      │    {name: "jira.getIssue",  │                              │          │
│      │     arguments: {...}}       │                              │          │
│      │                             │  ─────────────────────────>  │          │
│      │                             │    REST API Call             │          │
│      │                             │                              │          │
│      │                             │  <─────────────────────────  │          │
│      │                             │    API Response              │          │
│      │  <──────────────────────────│                              │          │
│      │    {content: [...]}         │                              │          │
│      │                             │                              │          │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. API vs MCP Decision Framework

### 4.1 Decision Matrix

| Factor | Prefer API | Prefer MCP |
|--------|------------|------------|
| **Existing Integration** | ✅ Well-tested, stable | Consider migration |
| **New Integration** | Simple, infrequent use | ✅ Standard pattern |
| **LLM Interaction** | Background/batch ops | ✅ Agent-driven ops |
| **Tool Discovery** | Fixed, known tools | ✅ Dynamic discovery |
| **Token Efficiency** | N/A | ✅ Critical concern |
| **Community Support** | Vendor-specific SDKs | ✅ MCP ecosystem |
| **Real-time Streaming** | Native WebSocket | ✅ SSE transport |
| **Low Latency** | ✅ Direct calls | Additional layer |
| **Credential Isolation** | Manual management | ✅ Server-side |

### 4.2 Integration Type Recommendations

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              HACI INTEGRATION TYPE RECOMMENDATIONS                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ╔═══════════════════════════════════════════════════════════════════════╗ │
│  ║  PREFER MCP (Agent-Driven Operations)                                  ║ │
│  ╠═══════════════════════════════════════════════════════════════════════╣ │
│  ║  • Ticketing: Jira, ServiceNow, PagerDuty                             ║ │
│  ║  • Code: GitHub, GitLab, Bitbucket                                    ║ │
│  ║  • Collaboration: Slack, Teams, Confluence                            ║ │
│  ║  • File Storage: Google Drive, S3, SharePoint                         ║ │
│  ║  • Knowledge: Notion, Confluence, Wiki                                ║ │
│  ╚═══════════════════════════════════════════════════════════════════════╝ │
│                                                                             │
│  ╔═══════════════════════════════════════════════════════════════════════╗ │
│  ║  PREFER DIRECT API (Performance-Critical)                              ║ │
│  ╠═══════════════════════════════════════════════════════════════════════╣ │
│  ║  • Databases: PostgreSQL, MySQL, MongoDB (direct connections)         ║ │
│  ║  • High-Volume Streaming: Kafka, RabbitMQ                             ║ │
│  ║  • Real-time Metrics: Prometheus scraping                             ║ │
│  ║  • LLM Providers: Anthropic, OpenAI (native SDKs)                     ║ │
│  ╚═══════════════════════════════════════════════════════════════════════╝ │
│                                                                             │
│  ╔═══════════════════════════════════════════════════════════════════════╗ │
│  ║  HYBRID (API + MCP)                                                    ║ │
│  ╠═══════════════════════════════════════════════════════════════════════╣ │
│  ║  • Monitoring: Datadog, New Relic (API for data, MCP for discovery)   ║ │
│  ║  • Cloud: AWS, Azure, GCP (API for infra, MCP for agent queries)      ║ │
│  ║  • Kubernetes: Direct API + MCP for agent exploration                 ║ │
│  ╚═══════════════════════════════════════════════════════════════════════╝ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Migration Strategy

For existing API integrations, HACI will follow a phased migration approach:

```
Phase 1: Identify Candidates
    │
    ├── High LLM interaction frequency
    ├── Tool discovery requirements
    ├── Community MCP server available
    └── Token efficiency gains > 50%
    
Phase 2: Parallel Implementation
    │
    ├── Deploy MCP server alongside API
    ├── Route agent traffic to MCP
    ├── Maintain API for batch operations
    └── Compare performance metrics
    
Phase 3: Gradual Migration
    │
    ├── Increase MCP traffic percentage
    ├── Validate reliability (99.9% target)
    ├── Document any feature gaps
    └── Plan gap resolution
    
Phase 4: API Deprecation
    │
    ├── Full MCP for agent operations
    ├── API retained for admin/batch
    └── Remove redundant API code
```

---

## 5. HACI MCP Server Architecture

### 5.1 Custom MCP Servers for HACI

While HACI will leverage community MCP servers where available, several custom servers are needed:

```python
# HACI Custom MCP Server: Context Bus Integration

from mcp import Server, Tool, Resource
from mcp.types import TextContent
import asyncio

class HACIContextBusMCPServer:
    """
    MCP Server for HACI's internal Context Bus
    Allows agents to share findings via MCP protocol
    """
    
    def __init__(self, redis_client):
        self.redis = redis_client
        self.server = Server("haci-context-bus")
        self._register_tools()
        self._register_resources()
    
    def _register_tools(self):
        """Register Context Bus tools"""
        
        @self.server.tool("context.publish")
        async def publish_finding(
            ticket_id: str,
            agent_id: str,
            finding: dict,
            confidence: float
        ) -> dict:
            """Publish agent finding to Context Bus"""
            key = f"findings:{ticket_id}:{agent_id}"
            await self.redis.setex(
                key,
                3600,  # 1 hour TTL
                json.dumps({
                    "finding": finding,
                    "confidence": confidence,
                    "timestamp": datetime.utcnow().isoformat()
                })
            )
            return {"success": True, "key": key}
        
        @self.server.tool("context.get_findings")
        async def get_findings(ticket_id: str) -> list:
            """Get all findings for a ticket"""
            pattern = f"findings:{ticket_id}:*"
            keys = await self.redis.keys(pattern)
            findings = []
            for key in keys:
                data = await self.redis.get(key)
                if data:
                    findings.append(json.loads(data))
            return findings
        
        @self.server.tool("context.subscribe")
        async def subscribe_to_updates(ticket_id: str):
            """Subscribe to real-time finding updates"""
            channel = f"updates:{ticket_id}"
            pubsub = self.redis.pubsub()
            await pubsub.subscribe(channel)
            return {"subscribed": channel}
    
    def _register_resources(self):
        """Register Context Bus resources"""
        
        @self.server.resource("context://findings/{ticket_id}")
        async def get_ticket_findings(ticket_id: str) -> str:
            """Resource: All findings for a ticket"""
            findings = await self.get_findings(ticket_id)
            return json.dumps(findings, indent=2)
        
        @self.server.resource("context://agents/active")
        async def get_active_agents() -> str:
            """Resource: Currently active agents"""
            keys = await self.redis.keys("agent:*:status")
            agents = []
            for key in keys:
                status = await self.redis.get(key)
                agents.append({
                    "agent_id": key.split(":")[1],
                    "status": status
                })
            return json.dumps(agents, indent=2)
```

### 5.2 MCP Server Registry

HACI maintains a registry of all available MCP servers:

```yaml
# config/mcp_servers.yaml

mcp_servers:
  # Community MCP Servers (from modelcontextprotocol.io)
  community:
    - name: github
      url: npx -y @modelcontextprotocol/server-github
      transport: stdio
      env:
        GITHUB_TOKEN: ${GITHUB_TOKEN}
      capabilities:
        - tools
        - resources
      
    - name: postgres
      url: npx -y @modelcontextprotocol/server-postgres
      transport: stdio
      env:
        DATABASE_URL: ${POSTGRES_URL}
      capabilities:
        - tools
        - resources
      
    - name: slack
      url: npx -y @modelcontextprotocol/server-slack
      transport: stdio
      env:
        SLACK_BOT_TOKEN: ${SLACK_BOT_TOKEN}
      capabilities:
        - tools
        - resources
        - prompts
  
  # Custom HACI MCP Servers
  custom:
    - name: haci-context-bus
      url: python -m haci.mcp.context_bus
      transport: stdio
      capabilities:
        - tools
        - resources
      
    - name: haci-orchestrator
      url: python -m haci.mcp.orchestrator
      transport: http
      http_endpoint: http://localhost:8080/mcp
      capabilities:
        - tools
        - prompts
        - sampling
    
    - name: haci-knowledge-base
      url: python -m haci.mcp.knowledge_base
      transport: stdio
      capabilities:
        - tools
        - resources
        - prompts
  
  # Enterprise MCP Servers (Remote)
  enterprise:
    - name: jira-enterprise
      url: https://mcp.company.com/jira/sse
      transport: sse
      auth:
        type: oauth2
        token_url: https://auth.company.com/oauth/token
      capabilities:
        - tools
        - resources
    
    - name: datadog-mcp
      url: https://mcp.datadoghq.com/v1/sse
      transport: sse
      auth:
        type: api_key
        header: DD-API-KEY
      capabilities:
        - tools
        - resources
```

---

## 6. HACI MCP Client Implementation

### 6.1 MCP Client Manager

```python
# haci/mcp/client_manager.py

from mcp import Client, StdioClientTransport, SSEClientTransport
from typing import Dict, List, Optional, Any
import asyncio
import yaml

class MCPClientManager:
    """
    Manages MCP client connections for HACI
    Handles server discovery, connection pooling, and tool routing
    """
    
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.clients: Dict[str, Client] = {}
        self.tool_registry: Dict[str, str] = {}  # tool_name -> server_name
        self.resource_registry: Dict[str, str] = {}
        
    async def initialize(self):
        """Initialize all MCP server connections"""
        for server_config in self._get_all_servers():
            await self._connect_server(server_config)
        
        # Build tool/resource routing tables
        await self._build_registries()
    
    async def _connect_server(self, config: Dict) -> Optional[Client]:
        """Establish connection to an MCP server"""
        try:
            transport = self._create_transport(config)
            client = Client(config["name"], transport)
            
            # Initialize with capabilities negotiation
            result = await client.initialize()
            
            self.clients[config["name"]] = client
            print(f"Connected to MCP server: {config['name']}")
            print(f"  Capabilities: {result.capabilities}")
            
            return client
        except Exception as e:
            print(f"Failed to connect to {config['name']}: {e}")
            return None
    
    def _create_transport(self, config: Dict):
        """Create appropriate transport based on config"""
        transport_type = config.get("transport", "stdio")
        
        if transport_type == "stdio":
            return StdioClientTransport(
                command=config["url"],
                env=config.get("env", {})
            )
        elif transport_type == "sse":
            return SSEClientTransport(
                url=config["url"],
                headers=self._get_auth_headers(config)
            )
        elif transport_type == "http":
            return HTTPClientTransport(
                endpoint=config["http_endpoint"],
                headers=self._get_auth_headers(config)
            )
        else:
            raise ValueError(f"Unknown transport type: {transport_type}")
    
    async def _build_registries(self):
        """Build routing tables for tools and resources"""
        for name, client in self.clients.items():
            # Get tools from server
            tools_result = await client.list_tools()
            for tool in tools_result.tools:
                self.tool_registry[tool.name] = name
            
            # Get resources from server
            resources_result = await client.list_resources()
            for resource in resources_result.resources:
                self.resource_registry[resource.uri] = name
    
    async def call_tool(
        self, 
        tool_name: str, 
        arguments: Dict[str, Any]
    ) -> Any:
        """Route tool call to appropriate MCP server"""
        server_name = self.tool_registry.get(tool_name)
        if not server_name:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        client = self.clients.get(server_name)
        if not client:
            raise RuntimeError(f"Server not connected: {server_name}")
        
        result = await client.call_tool(tool_name, arguments)
        return result
    
    async def read_resource(self, uri: str) -> Any:
        """Route resource read to appropriate MCP server"""
        # Find matching server by URI pattern
        for pattern, server_name in self.resource_registry.items():
            if self._matches_pattern(uri, pattern):
                client = self.clients.get(server_name)
                result = await client.read_resource(uri)
                return result
        
        raise ValueError(f"No server found for resource: {uri}")
    
    async def discover_tools(self, domain: Optional[str] = None) -> List[Dict]:
        """Discover available tools, optionally filtered by domain"""
        all_tools = []
        
        for name, client in self.clients.items():
            tools_result = await client.list_tools()
            for tool in tools_result.tools:
                tool_info = {
                    "name": tool.name,
                    "description": tool.description,
                    "server": name,
                    "schema": tool.inputSchema
                }
                
                if domain is None or self._tool_matches_domain(tool, domain):
                    all_tools.append(tool_info)
        
        return all_tools
    
    async def get_tool_definitions_for_agent(
        self, 
        agent_domain: str,
        max_tools: int = 20
    ) -> List[Dict]:
        """
        Get relevant tool definitions for an agent
        Uses domain matching and relevance scoring
        """
        domain_tools = await self.discover_tools(domain=agent_domain)
        
        # Sort by relevance and limit
        sorted_tools = sorted(
            domain_tools,
            key=lambda t: self._relevance_score(t, agent_domain),
            reverse=True
        )
        
        return sorted_tools[:max_tools]
```

### 6.2 Agent MCP Integration

```python
# haci/agents/mcp_enabled_agent.py

from haci.mcp.client_manager import MCPClientManager
from haci.agents.base import SpecializedAgent

class MCPEnabledAgent(SpecializedAgent):
    """
    Base class for agents that use MCP for tool access
    Implements efficient tool discovery and execution
    """
    
    def __init__(
        self,
        agent_id: str,
        domain: str,
        mcp_manager: MCPClientManager,
        model_router: ModelRouter
    ):
        super().__init__(agent_id, domain, model_router)
        self.mcp = mcp_manager
        self._cached_tools = None
        self._tool_cache_time = None
    
    async def get_available_tools(self, force_refresh: bool = False) -> List[Dict]:
        """Get tools available for this agent's domain"""
        # Use cached tools if recent
        if not force_refresh and self._cached_tools:
            cache_age = datetime.utcnow() - self._tool_cache_time
            if cache_age.seconds < 300:  # 5 minute cache
                return self._cached_tools
        
        # Discover tools for this domain
        tools = await self.mcp.get_tool_definitions_for_agent(
            agent_domain=self.domain,
            max_tools=20
        )
        
        self._cached_tools = tools
        self._tool_cache_time = datetime.utcnow()
        
        return tools
    
    async def execute_tool(
        self, 
        tool_name: str, 
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a tool via MCP"""
        try:
            result = await self.mcp.call_tool(tool_name, arguments)
            
            return {
                "success": True,
                "result": result.content,
                "tool": tool_name,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "tool": tool_name,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def act(self, action_plan: Dict) -> Dict:
        """
        ACT phase using MCP tools
        Executes actions from the THINK phase
        """
        results = []
        
        for action in action_plan.get("actions", []):
            tool_name = action["tool"]
            tool_params = action["params"]
            
            # Execute via MCP
            result = await self.execute_tool(tool_name, tool_params)
            results.append(result)
            
            # Publish to Context Bus if in swarm mode
            if self.execution_mode == ExecutionMode.SWARM:
                await self.mcp.call_tool(
                    "context.publish",
                    {
                        "ticket_id": self.current_ticket_id,
                        "agent_id": self.agent_id,
                        "finding": result,
                        "confidence": action.get("confidence", 0.7)
                    }
                )
        
        return {"results": results}
```

### 6.3 Code Execution Pattern for Efficiency

Following Anthropic's recommended pattern for MCP efficiency:

```python
# haci/mcp/code_execution.py

class MCPCodeExecutor:
    """
    Implements code execution pattern for efficient MCP usage
    Agents write code to interact with MCP servers
    """
    
    def __init__(self, mcp_manager: MCPClientManager):
        self.mcp = mcp_manager
        self.sandbox = CodeSandbox()
    
    async def execute_agent_code(
        self, 
        code: str, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute agent-generated code that interacts with MCP
        
        The code can:
        - Discover available tools
        - Read tool schemas
        - Call tools with parameters
        - Process results
        """
        # Inject MCP interface into sandbox
        sandbox_globals = {
            "mcp": MCPSandboxInterface(self.mcp),
            "context": context,
            "json": json,
            "datetime": datetime
        }
        
        # Execute in sandboxed environment
        result = await self.sandbox.execute(code, sandbox_globals)
        
        return result


class MCPSandboxInterface:
    """Safe interface to MCP for agent code execution"""
    
    def __init__(self, mcp_manager: MCPClientManager):
        self._mcp = mcp_manager
    
    async def list_servers(self) -> List[str]:
        """List available MCP server names"""
        return list(self._mcp.clients.keys())
    
    async def get_tools(self, server: str = None) -> List[Dict]:
        """Get tool definitions from specified server or all servers"""
        if server:
            client = self._mcp.clients.get(server)
            if client:
                result = await client.list_tools()
                return [{"name": t.name, "description": t.description} 
                        for t in result.tools]
        else:
            return await self._mcp.discover_tools()
    
    async def call(
        self, 
        tool: str, 
        **kwargs
    ) -> Any:
        """Call an MCP tool"""
        return await self._mcp.call_tool(tool, kwargs)
    
    async def read(self, uri: str) -> Any:
        """Read an MCP resource"""
        return await self._mcp.read_resource(uri)
```

**Example Agent Code Execution:**

```python
# Agent generates this code to investigate a database issue

code = '''
# Discover available database tools
db_tools = await mcp.get_tools("postgres")

# Get current connections
connections = await mcp.call(
    "postgres.query",
    query="SELECT * FROM pg_stat_activity WHERE state = 'active'"
)

# Get slow queries
slow_queries = await mcp.call(
    "postgres.query", 
    query="""
        SELECT query, calls, mean_time 
        FROM pg_stat_statements 
        ORDER BY mean_time DESC 
        LIMIT 5
    """
)

# Analyze and return findings
findings = {
    "active_connections": len(connections),
    "slow_queries": slow_queries,
    "recommendation": None
}

if len(connections) > 100:
    findings["recommendation"] = "Consider increasing max_connections"

return findings
'''

# Execute with ~50 tokens vs 150,000 for full tool definitions
result = await executor.execute_agent_code(code, {"ticket_id": "HACI-123"})
```

---

## 7. Integration Patterns by Domain

### 7.1 Ticketing Integration (MCP)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TICKETING INTEGRATION (MCP-PREFERRED)                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   HACI Agent                      MCP Server                    Jira API    │
│       │                               │                             │       │
│       │  ──tools/call──────────────>  │                             │       │
│       │   "jira.getIssue"             │                             │       │
│       │   {key: "HACI-123"}           │                             │       │
│       │                               │  ──GET /issue/HACI-123──>   │       │
│       │                               │                             │       │
│       │                               │  <──{issue data}────────    │       │
│       │  <──{content: [issue]}────    │                             │       │
│       │                               │                             │       │
│       │  ──tools/call──────────────>  │                             │       │
│       │   "jira.addComment"           │                             │       │
│       │   {key: "...",                │                             │       │
│       │    comment: "AI Analysis..."}│                             │       │
│       │                               │  ──POST /issue/.../comment─> │      │
│       │                               │                             │       │
│       │  <──{success: true}────────   │                             │       │
│                                                                             │
│   Benefits:                                                                 │
│   • Standardized interface across Jira/ServiceNow/PagerDuty               │
│   • Credential isolation in MCP server                                     │
│   • Tool discovery for agents                                              │
│   • Consistent error handling                                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Monitoring Integration (Hybrid)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MONITORING INTEGRATION (HYBRID)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │  MCP PATH (Agent-Driven Queries)                                      │  │
│   │                                                                       │  │
│   │  Log Agent ──> MCP Client ──> Datadog MCP Server ──> Datadog API     │  │
│   │                                                                       │  │
│   │  Used for:                                                           │  │
│   │  • Agent queries logs: "Find errors in last hour"                    │  │
│   │  • Dynamic metric exploration                                        │  │
│   │  • APM trace analysis                                                │  │
│   └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │  DIRECT API PATH (High-Volume Streaming)                              │  │
│   │                                                                       │  │
│   │  Metrics Collector ──> Datadog API ──> TimescaleDB                   │  │
│   │                                                                       │  │
│   │  Used for:                                                           │  │
│   │  • Continuous metric ingestion                                       │  │
│   │  • High-frequency log streaming                                      │  │
│   │  • Batch metric exports                                              │  │
│   └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│   Decision: Use MCP for agent queries, Direct API for streaming/batch       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.3 Database Integration (Direct API with MCP Discovery)

```python
# Pattern: Direct connections with MCP for discovery/metadata

class DatabaseIntegrationPattern:
    """
    Database pattern: Direct connection + MCP discovery
    
    Why hybrid:
    - Direct: Performance-critical queries need minimal latency
    - MCP: Schema discovery, metadata, agent exploration
    """
    
    def __init__(self):
        # Direct connection pool for queries
        self.pool = asyncpg.create_pool(...)
        
        # MCP for discovery and metadata
        self.mcp = MCPClientManager(...)
    
    async def execute_query(self, query: str) -> List[Dict]:
        """Direct execution for performance"""
        async with self.pool.acquire() as conn:
            return await conn.fetch(query)
    
    async def discover_schema(self) -> Dict:
        """MCP for schema exploration"""
        return await self.mcp.call_tool(
            "postgres.describe_schema",
            {}
        )
    
    async def get_table_info(self, table: str) -> Dict:
        """MCP for metadata queries"""
        return await self.mcp.read_resource(
            f"postgres://tables/{table}"
        )
```

### 7.4 Code Repository Integration (MCP-Preferred)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                CODE REPOSITORY INTEGRATION (MCP-PREFERRED)                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  GitHub MCP Server Capabilities:                                            │
│                                                                             │
│  TOOLS:                                                                     │
│  ├── github.getRepository      - Get repo information                      │
│  ├── github.getFile            - Read file contents                        │
│  ├── github.searchCode         - Search across repositories                │
│  ├── github.createPullRequest  - Create new PR                             │
│  ├── github.getPullRequest     - Get PR details                            │
│  ├── github.addPRComment       - Comment on PR                             │
│  ├── github.getWorkflowRuns    - Get CI/CD status                          │
│  └── github.getWorkflowLogs    - Get build logs                            │
│                                                                             │
│  RESOURCES:                                                                 │
│  ├── github://repos/{owner}/{repo}                                         │
│  ├── github://repos/{owner}/{repo}/files/{path}                            │
│  ├── github://repos/{owner}/{repo}/pulls                                   │
│  └── github://repos/{owner}/{repo}/actions                                 │
│                                                                             │
│  PROMPTS:                                                                   │
│  ├── analyze_pr       - Template for PR analysis                           │
│  ├── review_security  - Security-focused review                            │
│  └── suggest_fix      - Code fix suggestions                               │
│                                                                             │
│  Agent Usage Example:                                                       │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ Code Agent receives ticket about failing build                      │    │
│  │                                                                     │    │
│  │ 1. Get workflow runs:                                               │    │
│  │    result = await mcp.call("github.getWorkflowRuns",               │    │
│  │                            repo="org/app", status="failure")        │    │
│  │                                                                     │    │
│  │ 2. Get failure logs:                                                │    │
│  │    logs = await mcp.call("github.getWorkflowLogs",                 │    │
│  │                          repo="org/app", run_id=result[0].id)       │    │
│  │                                                                     │    │
│  │ 3. Analyze and find root cause                                      │    │
│  │                                                                     │    │
│  │ 4. Create comment with findings:                                    │    │
│  │    await mcp.call("github.addPRComment",                           │    │
│  │                   repo="org/app", pr=123, body="Analysis...")       │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Security and Authentication

### 8.1 API Security Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    HACI SECURITY ARCHITECTURE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                        ┌─────────────────────┐                              │
│                        │   HASHICORP VAULT   │                              │
│                        │   (Secrets Store)   │                              │
│                        └──────────┬──────────┘                              │
│                                   │                                         │
│           ┌───────────────────────┼───────────────────────┐                 │
│           │                       │                       │                 │
│           ▼                       ▼                       ▼                 │
│   ┌──────────────┐       ┌──────────────┐       ┌──────────────┐           │
│   │ API Keys     │       │ OAuth Tokens │       │ Certificates │           │
│   │              │       │              │       │              │           │
│   │ Datadog      │       │ Jira         │       │ PostgreSQL   │           │
│   │ PagerDuty    │       │ GitHub       │       │ Kubernetes   │           │
│   │ New Relic    │       │ Slack        │       │ mTLS certs   │           │
│   └──────┬───────┘       └──────┬───────┘       └──────┬───────┘           │
│          │                      │                      │                    │
│          └──────────────────────┼──────────────────────┘                    │
│                                 │                                           │
│                                 ▼                                           │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                    CREDENTIAL INJECTION LAYER                        │  │
│   │                                                                      │  │
│   │  • Short-lived credential retrieval (< 1 hour)                      │  │
│   │  • Per-request credential injection                                 │  │
│   │  • Automatic rotation handling                                      │  │
│   │  • Audit logging of all credential access                           │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                 │                                           │
│           ┌─────────────────────┼─────────────────────┐                    │
│           │                     │                     │                    │
│           ▼                     ▼                     ▼                    │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐              │
│   │ API Adapter  │     │ MCP Server   │     │ Direct DB    │              │
│   │ (Jira, etc)  │     │ (GitHub,etc) │     │ Connection   │              │
│   └──────────────┘     └──────────────┘     └──────────────┘              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 8.2 MCP Security Considerations

```python
# haci/mcp/security.py

class MCPSecurityManager:
    """
    Security manager for MCP operations
    Implements Anthropic's MCP security recommendations
    """
    
    def __init__(self, vault_client):
        self.vault = vault_client
        self.permission_cache = TTLCache(maxsize=1000, ttl=300)
    
    async def validate_tool_call(
        self, 
        agent_id: str, 
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate tool call against security policy
        
        MCP Security Principles:
        1. Tool descriptions are untrusted
        2. Human approval for sensitive operations
        3. Least privilege access
        """
        # Check agent permissions for this tool
        permissions = await self._get_agent_permissions(agent_id)
        if tool_name not in permissions.allowed_tools:
            return False, f"Agent {agent_id} not authorized for {tool_name}"
        
        # Check for sensitive operations requiring approval
        if self._is_sensitive_operation(tool_name, arguments):
            approval = await self._request_human_approval(
                agent_id, tool_name, arguments
            )
            if not approval.granted:
                return False, "Human approval denied"
        
        # Validate arguments against schema
        valid, error = await self._validate_arguments(tool_name, arguments)
        if not valid:
            return False, error
        
        return True, None
    
    def _is_sensitive_operation(
        self, 
        tool_name: str, 
        arguments: Dict
    ) -> bool:
        """Determine if operation requires human approval"""
        sensitive_patterns = [
            # Write operations
            ("*.create*", lambda a: True),
            ("*.delete*", lambda a: True),
            ("*.update*", lambda a: True),
            
            # Specific high-risk operations
            ("jira.transition", lambda a: a.get("status") == "Closed"),
            ("github.merge*", lambda a: True),
            ("postgres.execute", lambda a: "DROP" in a.get("query", "").upper()),
            ("aws.terminate*", lambda a: True),
        ]
        
        for pattern, condition in sensitive_patterns:
            if fnmatch.fnmatch(tool_name, pattern):
                if condition(arguments):
                    return True
        
        return False
    
    async def inject_credentials(
        self, 
        server_name: str
    ) -> Dict[str, str]:
        """
        Inject credentials for MCP server
        Credentials are short-lived and scoped
        """
        creds_path = f"secret/haci/mcp/{server_name}"
        
        # Get from Vault with 1-hour lease
        secret = await self.vault.secrets.kv.v2.read_secret(
            path=creds_path,
            mount_point="secret"
        )
        
        # Log credential access
        await self._audit_log(
            event="credential_access",
            server=server_name,
            timestamp=datetime.utcnow()
        )
        
        return secret.data
```

### 8.3 OAuth 2.0 Flow for MCP Servers

```python
# OAuth configuration for enterprise MCP servers

oauth_config = {
    "jira_enterprise": {
        "authorization_url": "https://auth.atlassian.com/authorize",
        "token_url": "https://auth.atlassian.com/oauth/token",
        "scopes": [
            "read:jira-work",
            "write:jira-work", 
            "read:jira-user"
        ],
        "refresh_enabled": True,
        "token_expiry": 3600
    },
    "github_enterprise": {
        "authorization_url": "https://github.com/login/oauth/authorize",
        "token_url": "https://github.com/login/oauth/access_token",
        "scopes": [
            "repo",
            "read:org",
            "workflow"
        ],
        "refresh_enabled": False,
        "token_expiry": None  # GitHub tokens don't expire by default
    }
}
```

---

## 9. Performance and Optimization

### 9.1 Token Efficiency Metrics

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TOKEN EFFICIENCY COMPARISON                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Scenario: Agent investigating database issue                               │
│  Needs: Query DB, check logs, update ticket                                 │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────────┐│
│  │ TRADITIONAL API (All Tools in Prompt)                                   ││
│  │                                                                         ││
│  │ Tool Definitions Loaded:                                                ││
│  │ ├── Jira tools (15 tools)         ~3,000 tokens                        ││
│  │ ├── Datadog tools (12 tools)      ~2,500 tokens                        ││
│  │ ├── PostgreSQL tools (8 tools)    ~1,800 tokens                        ││
│  │ ├── GitHub tools (10 tools)       ~2,200 tokens                        ││
│  │ └── AWS tools (20 tools)          ~4,500 tokens                        ││
│  │                                                                         ││
│  │ Total Tool Definitions:           ~14,000 tokens                        ││
│  │ System Prompt:                    ~2,000 tokens                         ││
│  │ Conversation Context:             ~3,000 tokens                         ││
│  │                                                                         ││
│  │ TOTAL PER REQUEST:                ~19,000 tokens                        ││
│  │ Cost per request @ $3/1M:         $0.057                                ││
│  └────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────────┐│
│  │ MCP CODE EXECUTION (On-Demand Discovery)                                ││
│  │                                                                         ││
│  │ Agent discovers and loads only needed tools:                            ││
│  │ ├── postgres.query (1 tool)       ~400 tokens                          ││
│  │ ├── datadog.searchLogs (1 tool)   ~350 tokens                          ││
│  │ └── jira.addComment (1 tool)      ~300 tokens                          ││
│  │                                                                         ││
│  │ Total Tool Definitions:           ~1,050 tokens                         ││
│  │ System Prompt:                    ~2,000 tokens                         ││
│  │ Conversation Context:             ~3,000 tokens                         ││
│  │                                                                         ││
│  │ TOTAL PER REQUEST:                ~6,050 tokens                         ││
│  │ Cost per request @ $3/1M:         $0.018                                ││
│  └────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│  SAVINGS: 68% token reduction, 68% cost reduction                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Caching Strategy

```python
# haci/mcp/caching.py

from cachetools import TTLCache, LRUCache
from typing import Any, Optional

class MCPCacheManager:
    """
    Multi-layer caching for MCP operations
    """
    
    def __init__(self):
        # Tool definitions cache (change infrequently)
        self.tool_cache = TTLCache(maxsize=100, ttl=3600)  # 1 hour
        
        # Resource content cache (varies by resource)
        self.resource_cache = TTLCache(maxsize=500, ttl=300)  # 5 minutes
        
        # Results cache (short-lived)
        self.result_cache = LRUCache(maxsize=1000)
        
        # Cache statistics
        self.stats = {"hits": 0, "misses": 0}
    
    async def get_tools(
        self, 
        server: str, 
        client: MCPClient
    ) -> List[Dict]:
        """Get tools with caching"""
        cache_key = f"tools:{server}"
        
        if cache_key in self.tool_cache:
            self.stats["hits"] += 1
            return self.tool_cache[cache_key]
        
        self.stats["misses"] += 1
        tools = await client.list_tools()
        self.tool_cache[cache_key] = tools.tools
        
        return tools.tools
    
    async def get_resource(
        self, 
        uri: str, 
        client: MCPClient,
        ttl_override: Optional[int] = None
    ) -> Any:
        """Get resource with adaptive caching"""
        cache_key = f"resource:{uri}"
        
        if cache_key in self.resource_cache:
            self.stats["hits"] += 1
            return self.resource_cache[cache_key]
        
        self.stats["misses"] += 1
        content = await client.read_resource(uri)
        
        # Store with optional TTL override
        if ttl_override:
            self.resource_cache.update({cache_key: content}, ttl=ttl_override)
        else:
            self.resource_cache[cache_key] = content
        
        return content
    
    def invalidate_server(self, server: str):
        """Invalidate all caches for a server"""
        # Clear tool cache for server
        keys_to_remove = [k for k in self.tool_cache if k.startswith(f"tools:{server}")]
        for key in keys_to_remove:
            del self.tool_cache[key]
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total = self.stats["hits"] + self.stats["misses"]
        hit_rate = self.stats["hits"] / total if total > 0 else 0
        
        return {
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "hit_rate": f"{hit_rate:.2%}",
            "tool_cache_size": len(self.tool_cache),
            "resource_cache_size": len(self.resource_cache)
        }
```

### 9.3 Connection Pooling

```python
# haci/mcp/connection_pool.py

import asyncio
from contextlib import asynccontextmanager

class MCPConnectionPool:
    """
    Connection pool for MCP servers
    Manages persistent connections with health checking
    """
    
    def __init__(self, max_connections_per_server: int = 5):
        self.max_connections = max_connections_per_server
        self.pools: Dict[str, asyncio.Queue] = {}
        self.health_check_interval = 30
        self._health_task = None
    
    async def initialize(self, server_configs: List[Dict]):
        """Initialize connection pools for all servers"""
        for config in server_configs:
            server_name = config["name"]
            self.pools[server_name] = asyncio.Queue(maxsize=self.max_connections)
            
            # Pre-populate pool
            for _ in range(self.max_connections):
                conn = await self._create_connection(config)
                await self.pools[server_name].put(conn)
        
        # Start health check task
        self._health_task = asyncio.create_task(self._health_check_loop())
    
    @asynccontextmanager
    async def get_connection(self, server_name: str):
        """Get a connection from pool, return when done"""
        pool = self.pools.get(server_name)
        if not pool:
            raise ValueError(f"Unknown server: {server_name}")
        
        # Get connection (wait if none available)
        conn = await asyncio.wait_for(pool.get(), timeout=30)
        
        try:
            yield conn
        finally:
            # Return to pool if healthy
            if await self._is_healthy(conn):
                await pool.put(conn)
            else:
                # Replace with new connection
                new_conn = await self._create_connection(conn.config)
                await pool.put(new_conn)
    
    async def _health_check_loop(self):
        """Periodic health check of all connections"""
        while True:
            await asyncio.sleep(self.health_check_interval)
            
            for server_name, pool in self.pools.items():
                # Check each connection in pool
                healthy_conns = []
                
                while not pool.empty():
                    conn = await pool.get()
                    if await self._is_healthy(conn):
                        healthy_conns.append(conn)
                    else:
                        # Replace unhealthy connection
                        new_conn = await self._create_connection(conn.config)
                        healthy_conns.append(new_conn)
                
                # Return connections to pool
                for conn in healthy_conns:
                    await pool.put(conn)
```

---

## 10. Implementation Roadmap

### 10.1 Phase 1: Foundation (Weeks 1-8)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: FOUNDATION (Weeks 1-8)                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Week 1-2: MCP Infrastructure Setup                                         │
│  ├── Deploy MCP Client Manager                                              │
│  ├── Configure community MCP servers (GitHub, Postgres, Slack)              │
│  ├── Set up Vault integration for credentials                               │
│  └── Implement connection pooling                                           │
│                                                                             │
│  Week 3-4: Core MCP Servers                                                 │
│  ├── Deploy Jira MCP Server (community or custom)                          │
│  ├── Deploy Datadog MCP Server (custom)                                    │
│  ├── Implement HACI Context Bus MCP Server                                 │
│  └── Test tool discovery and execution                                     │
│                                                                             │
│  Week 5-6: Agent MCP Integration                                            │
│  ├── Refactor agents to use MCPEnabledAgent base class                     │
│  ├── Implement code execution pattern                                      │
│  ├── Add caching layer                                                     │
│  └── Test agent-MCP communication                                          │
│                                                                             │
│  Week 7-8: Security & Testing                                               │
│  ├── Implement MCPSecurityManager                                          │
│  ├── Set up audit logging                                                  │
│  ├── Integration testing                                                   │
│  └── Performance benchmarking                                              │
│                                                                             │
│  Deliverables:                                                              │
│  ✓ MCP infrastructure operational                                          │
│  ✓ 5 MCP servers deployed (GitHub, Postgres, Slack, Jira, Datadog)        │
│  ✓ All agents MCP-enabled                                                  │
│  ✓ 50%+ token reduction achieved                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 10.2 Phase 2: Expansion (Weeks 9-16)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 2: EXPANSION (Weeks 9-16)                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Week 9-10: Additional MCP Servers                                          │
│  ├── ServiceNow MCP Server                                                 │
│  ├── PagerDuty MCP Server                                                  │
│  ├── AWS MCP Server (custom)                                               │
│  └── New Relic MCP Server                                                  │
│                                                                             │
│  Week 11-12: Enterprise Features                                            │
│  ├── SSE transport for remote MCP servers                                  │
│  ├── OAuth 2.0 integration                                                 │
│  ├── Multi-tenant credential isolation                                     │
│  └── High availability configuration                                       │
│                                                                             │
│  Week 13-14: Knowledge Base MCP                                             │
│  ├── HACI Knowledge Base MCP Server                                        │
│  ├── Runbook resources                                                     │
│  ├── Prompt templates for common issues                                    │
│  └── Documentation search tools                                            │
│                                                                             │
│  Week 15-16: Optimization                                                   │
│  ├── Advanced caching strategies                                           │
│  ├── Connection pool tuning                                                │
│  ├── Token efficiency optimization                                         │
│  └── Load testing at scale                                                 │
│                                                                             │
│  Deliverables:                                                              │
│  ✓ 10+ MCP servers operational                                             │
│  ✓ Enterprise-grade security                                               │
│  ✓ Knowledge base fully integrated                                         │
│  ✓ 70%+ token reduction achieved                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 10.3 Phase 3: Maturity (Weeks 17-24)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 3: MATURITY (Weeks 17-24)                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Week 17-18: API Migration                                                  │
│  ├── Identify remaining direct API integrations                            │
│  ├── Create MCP wrappers where beneficial                                  │
│  ├── Deprecation plan for redundant APIs                                   │
│  └── Documentation updates                                                 │
│                                                                             │
│  Week 19-20: Sampling Implementation                                        │
│  ├── MCP Sampling for nested agent calls                                   │
│  ├── Human approval integration                                            │
│  ├── Sampling quota management                                             │
│  └── Cost tracking for sampling                                            │
│                                                                             │
│  Week 21-22: Advanced Patterns                                              │
│  ├── Multi-server orchestration                                            │
│  ├── Cross-server transactions                                             │
│  ├── Streaming results                                                     │
│  └── Real-time notifications                                               │
│                                                                             │
│  Week 23-24: Production Hardening                                           │
│  ├── Chaos testing                                                         │
│  ├── Failover testing                                                      │
│  ├── Performance optimization                                              │
│  └── Final documentation                                                   │
│                                                                             │
│  Deliverables:                                                              │
│  ✓ Full MCP ecosystem operational                                          │
│  ✓ API/MCP hybrid strategy documented                                      │
│  ✓ Production-ready with 99.9% uptime                                      │
│  ✓ Complete documentation and runbooks                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 11. Appendices

### 11.1 MCP Server Reference Table

| Server | Type | Transport | Priority | Tools | Resources | Prompts |
|--------|------|-----------|----------|-------|-----------|---------|
| GitHub | Community | stdio | P0 | 15 | 8 | 3 |
| Postgres | Community | stdio | P0 | 10 | 5 | 2 |
| Slack | Community | stdio | P1 | 12 | 6 | 4 |
| Jira | Custom | SSE | P0 | 18 | 10 | 5 |
| Datadog | Custom | SSE | P0 | 14 | 8 | 3 |
| ServiceNow | Custom | SSE | P1 | 16 | 9 | 4 |
| HACI Context Bus | Custom | stdio | P0 | 8 | 4 | 0 |
| HACI KB | Custom | stdio | P0 | 6 | 12 | 8 |

### 11.2 API vs MCP Quick Reference

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       QUICK DECISION REFERENCE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  USE MCP WHEN:                          USE DIRECT API WHEN:               │
│  ✓ Agent needs to discover tools        ✓ Fixed, known operations         │
│  ✓ Reducing token usage is critical     ✓ Sub-millisecond latency needed  │
│  ✓ Multiple vendors in same category    ✓ High-volume batch operations    │
│  ✓ Building new integrations            ✓ Existing stable integration     │
│  ✓ Need prompt templates                ✓ Direct database queries         │
│  ✓ Want credential isolation            ✓ Real-time streaming data        │
│                                                                             │
│  ALWAYS MCP:                            ALWAYS DIRECT API:                 │
│  • Ticketing (Jira, ServiceNow)         • PostgreSQL/MySQL queries        │
│  • Code repos (GitHub, GitLab)          • LLM provider calls              │
│  • Collaboration (Slack, Teams)         • Message queue publishing        │
│  • File storage (GDrive, S3)            • Metrics streaming               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 11.3 Glossary

| Term | Definition |
|------|------------|
| **MCP** | Model Context Protocol - Open standard for connecting AI to external systems |
| **MCP Server** | Service that exposes tools, resources, and prompts via MCP |
| **MCP Client** | Component that connects to MCP servers (HACI agents) |
| **Tool** | Executable function exposed by MCP server |
| **Resource** | Structured data source accessible via MCP |
| **Prompt** | Instruction template provided by MCP server |
| **Sampling** | MCP feature allowing servers to request LLM completions |
| **stdio** | MCP transport using standard input/output |
| **SSE** | Server-Sent Events - MCP transport for remote servers |
| **Context Bus** | HACI's Redis-based message bus for agent coordination |

---

**Document Status:** Active  
**Maintained By:** HACI Architecture Team  
**Review Cycle:** Monthly  
**Last Updated:** December 2025
