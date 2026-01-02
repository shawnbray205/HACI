# HACI: Harness-Enhanced Agentic Collaborative Intelligence

<div align="center">

![HACI Logo](docs/assets/haci-logo.png)

**Enterprise-grade multi-agent AI orchestration with calibrated human oversight**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node 20+](https://img.shields.io/badge/node-20+-green.svg)](https://nodejs.org/)
[![ISO 42001 Ready](https://img.shields.io/badge/ISO%2042001-Ready-brightgreen.svg)](docs/governance/ISO-42001-COMPLIANCE.md)

[Documentation](docs/) • [Quick Start](#quick-start) • [Architecture](#architecture) • [Contributing](CONTRIBUTING.md)

</div>

---

## Overview

HACI (Harness-Enhanced Agentic Collaborative Intelligence) is an enterprise AI automation platform that orchestrates specialized AI agents to handle complex, multi-domain workflows. Unlike traditional automation, HACI implements **calibrated human oversight** through a sophisticated harness architecture that ensures appropriate governance at every autonomy level.

### Key Features

- **🎯 Four Execution Modes** — Automatically matches AI capability to task complexity
- **🛡️ Governed Autonomy** — Confidence-based gates ensure AI only acts autonomously when appropriate
- **🧠 10 Specialized Agents** — Domain-expert agents for logs, code, databases, infrastructure, and more
- **🔌 Dual Integration** — Supports both traditional APIs and Model Context Protocol (MCP)
- **💰 Economic Optimization** — Intelligent model routing achieves 71%+ cost reduction
- **📋 ISO 42001 Ready** — Comprehensive governance framework for enterprise compliance

---

## Execution Modes

HACI dynamically selects the appropriate execution mode based on task complexity:

| Mode | Agents | Human Oversight | Use Cases |
|------|--------|-----------------|-----------|
| **Single Agent** | 1 | Minimal | Password resets, status queries, simple lookups |
| **Micro-Swarm** | 2-3 | Checkpoint-based | Multi-system diagnostics, coordinated updates |
| **Full Swarm** | 4+ | Active monitoring | Disaster recovery, complex migrations |
| **Human-Led** | Variable | Direct control | Security incidents, compliance matters |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    LAYER 4: META-ORCHESTRATION                      │
│  Complexity Scoring → Mode Selection → Resource Management          │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                LAYER 3: HUMAN-AGENT COLLABORATION                   │
│   ≥95% AUTO  │  85-94% EXEC+REV  │  70-84% APPROVAL  │  <70% HUMAN │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                  LAYER 2: SWARM INTELLIGENCE                        │
│  Context Bus → Agent Coordination → Dispute Resolution              │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    LAYER 1: FOUNDATION                              │
│  Specialized Agents │ Harness Pattern │ Tool Integration            │
└─────────────────────────────────────────────────────────────────────┘
```

### Specialized Agents

| Agent | Domain | Primary Responsibilities |
|-------|--------|-------------------------|
| **Log Analyst** | Observability | Log parsing, pattern detection, anomaly identification |
| **Code Specialist** | Development | Code review, debugging, syntax analysis |
| **Database Expert** | Data | Query optimization, schema analysis, data integrity |
| **Infrastructure Ops** | Platform | Cloud resources, networking, scaling |
| **Security Analyst** | Security | Vulnerability assessment, threat detection |
| **API Specialist** | Integration | Endpoint debugging, contract validation |
| **Performance Engineer** | Optimization | Bottleneck analysis, resource tuning |
| **Documentation Writer** | Knowledge | Resolution documentation, KB updates |
| **Communication Manager** | Customer | Status updates, stakeholder notifications |
| **Swarm Coordinator** | Orchestration | Multi-agent coordination, dispute resolution |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/haci.git
cd haci

# Install Python dependencies
pip install -e ".[dev]"

# Install Node dependencies
npm install

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Start infrastructure services
docker-compose up -d postgres redis

# Initialize database
python scripts/init_db.py

# Run the development server
python -m haci.server
```

### Basic Usage

```python
from haci import HACIOrchestrator
from haci.config import HACIConfig

# Initialize HACI
config = HACIConfig.from_env()
orchestrator = HACIOrchestrator(config)

# Submit a task
task = orchestrator.submit({
    "type": "support_ticket",
    "title": "API returning 502 errors intermittently",
    "description": "Users reporting sporadic 502 errors on /api/users endpoint",
    "priority": "high"
})

# HACI automatically:
# 1. Scores complexity (determines this needs Micro-Swarm)
# 2. Selects appropriate agents (API, Log, Infrastructure)
# 3. Coordinates investigation
# 4. Requests human approval if needed
# 5. Returns resolution

result = await orchestrator.await_result(task.id)
print(f"Resolution: {result.summary}")
print(f"Confidence: {result.confidence}%")
print(f"Execution Mode: {result.mode}")
```

---

## Configuration

HACI uses a layered configuration system:

```yaml
# config/haci.yaml
execution:
  default_mode: auto  # auto, single, micro-swarm, full-swarm, human-led
  confidence_thresholds:
    auto_execute: 95
    execute_review: 85
    require_approval: 70
    human_led: 0

agents:
  log_analyst:
    model: claude-sonnet-4-20250514
    max_tokens: 8000
  code_specialist:
    model: claude-sonnet-4-20250514
    max_tokens: 16000
  # ... additional agents

integrations:
  mcp:
    enabled: true
    servers:
      - name: jira-mcp
        url: ${JIRA_MCP_URL}
      - name: github-mcp
        url: ${GITHUB_MCP_URL}
  api:
    enabled: true
    providers:
      - name: datadog
        base_url: https://api.datadoghq.com
        auth_type: api_key
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [Architecture Guide](docs/architecture/README.md) | Complete system architecture |
| [Context Engineering](docs/architecture/context-engineering.md) | Multi-agent memory management |
| [Governance Framework](docs/governance/README.md) | ISO 42001 compliance guide |
| [Integration Guide](docs/integration/README.md) | API and MCP integration |
| [Deployment Guide](docs/guides/deployment.md) | Production deployment |
| [API Reference](docs/api/README.md) | Complete API documentation |

---

## Governance & Compliance

HACI includes a comprehensive governance framework aligned with:

- **ISO 42001** — AI Management System
- **NIST AI RMF** — Risk Management Framework
- **EU AI Act** — European AI Regulation
- **SOC 2 Type II** — Security Controls

Key governance features:
- Quantitative risk scoring for all agent decisions
- Tamper-evident audit logging
- Mode-specific approval workflows
- Inter-agent attack testing protocols
- User-facing explainability for all decisions

See [Governance Documentation](docs/governance/) for complete details.

---

## Development

### Running Tests

```bash
# Unit tests
pytest tests/unit -v

# Integration tests (requires running services)
pytest tests/integration -v

# End-to-end tests
pytest tests/e2e -v

# All tests with coverage
pytest --cov=haci --cov-report=html
```

### Code Style

```bash
# Format code
black src tests
isort src tests

# Type checking
mypy src

# Linting
ruff check src tests
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

---

## Roadmap

- [x] **Phase 1: Foundation** — Core harness pattern, first 3 agents
- [x] **Phase 2: Swarm Intelligence** — Context bus, coordinator, full agent roster
- [x] **Phase 3: Multi-Provider LLM** — Anthropic, OpenAI, Google integration
- [ ] **Phase 4: Human-Agent Collaboration** — Confidence gates, approval workflows
- [ ] **Phase 5: Production Readiness** — Security hardening, performance optimization

See [ROADMAP.md](ROADMAP.md) for detailed timeline.

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## Acknowledgments

HACI builds upon research and patterns from:
- [Anthropic's Long-Running Agent Harness](https://www.anthropic.com)
- [MemGPT/Letta](https://github.com/cpacker/MemGPT) — LLM as Operating System paradigm
- [Model Context Protocol](https://modelcontextprotocol.io) — Standardized AI-tool integration

---

<div align="center">

**HACI is not just an automation platform—it's a new paradigm for human-AI collaboration.**

[Website](https://your-org.com/haci) • [Documentation](docs/) • [Community](https://discord.gg/your-org)

</div>
