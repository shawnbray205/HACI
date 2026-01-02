# Changelog

All notable changes to HACI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Human approval dashboard (in progress)
- Notification system architecture

### Changed
- Improved confidence calculation algorithm

### Fixed
- Context bus memory leak under high load

## [0.1.0] - 2025-01-01

### Added
- Initial alpha release
- Core harness pattern implementation
- 10 specialized agents:
  - Log Analyst
  - Code Specialist
  - Database Expert
  - Infrastructure Ops
  - Security Analyst
  - API Specialist
  - Performance Engineer
  - Documentation Writer
  - Communication Manager
  - Swarm Coordinator
- Four execution modes:
  - Single Agent
  - Micro-Swarm
  - Full Swarm
  - Human-Led
- Meta-orchestrator with complexity scoring
- Context Bus for multi-agent communication
- Multi-provider LLM support (Anthropic, OpenAI, Google)
- Confidence-based action gating
- Basic CLI interface
- Docker and docker-compose setup
- Initial documentation

### Security
- Harness-based credential isolation
- Audit logging for all agent actions
- Rate limiting on API endpoints

---

## Version History

### Pre-release Development

#### Foundation Phase (Weeks 1-12)
- Established Kubernetes infrastructure
- Implemented core harness pattern
- Deployed first three agents

#### Swarm Intelligence Phase (Weeks 13-24)
- Built Context Bus
- Added remaining agents
- Implemented dispute resolution

#### Multi-Provider Phase (Weeks 25-32)
- Abstracted LLM interface
- Integrated three providers
- Added circuit breakers and fallbacks

---

[Unreleased]: https://github.com/your-org/haci/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/your-org/haci/releases/tag/v0.1.0
