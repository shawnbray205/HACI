# Contributing to HACI

Thank you for your interest in contributing to HACI! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Issues

Before submitting an issue, please:

1. **Search existing issues** to avoid duplicates
2. **Use the appropriate template** for bugs, features, or documentation
3. **Provide complete information** including environment, steps to reproduce, and expected vs actual behavior

### Submitting Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the coding standards** outlined below
3. **Write tests** for new functionality
4. **Update documentation** as needed
5. **Ensure CI passes** before requesting review

## Development Setup

### Prerequisites

```bash
# Required tools
python >= 3.11
node >= 20
docker
docker-compose
```

### Local Development

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/haci.git
cd haci

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in development mode
pip install -e ".[dev]"
npm install

# Install pre-commit hooks
pre-commit install

# Start infrastructure
docker-compose up -d postgres redis

# Run tests to verify setup
pytest tests/unit -v
```

## Coding Standards

### Python

- **Style**: Follow [PEP 8](https://pep8.org/) with [Black](https://black.readthedocs.io/) formatting
- **Imports**: Use [isort](https://pycqa.github.io/isort/) for import organization
- **Types**: Use type hints; run [mypy](https://mypy.readthedocs.io/) for validation
- **Linting**: Use [ruff](https://docs.astral.sh/ruff/) for linting

```bash
# Format and lint
black src tests
isort src tests
ruff check src tests --fix
mypy src
```

### TypeScript/JavaScript

- **Style**: Follow [Prettier](https://prettier.io/) formatting
- **Linting**: Use [ESLint](https://eslint.org/)

```bash
npm run format
npm run lint
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, etc.)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvement
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(agents): add new Database Expert agent
fix(harness): resolve confidence calculation overflow
docs: update integration guide with MCP examples
```

## Testing Guidelines

### Test Structure

```
tests/
├── unit/              # Fast, isolated tests
│   ├── agents/        # Agent-specific tests
│   ├── harness/       # Harness pattern tests
│   └── orchestrator/  # Orchestration tests
├── integration/       # Tests requiring services
│   ├── api/           # API integration tests
│   └── mcp/           # MCP integration tests
└── e2e/               # Full workflow tests
```

### Writing Tests

```python
import pytest
from haci.agents import LogAnalyst
from haci.harness import Harness

class TestLogAnalyst:
    """Tests for the Log Analyst agent."""
    
    @pytest.fixture
    def agent(self) -> LogAnalyst:
        """Create a test agent instance."""
        return LogAnalyst(config=test_config())
    
    def test_log_parsing(self, agent: LogAnalyst) -> None:
        """Verify log parsing extracts correct fields."""
        log_entry = "2024-01-15 10:30:45 ERROR [api.users] Connection timeout"
        result = agent.parse_log(log_entry)
        
        assert result.timestamp == "2024-01-15 10:30:45"
        assert result.level == "ERROR"
        assert result.source == "api.users"
        assert "timeout" in result.message.lower()
    
    @pytest.mark.asyncio
    async def test_anomaly_detection(self, agent: LogAnalyst) -> None:
        """Verify anomaly detection identifies patterns."""
        logs = load_test_logs("anomaly_sample.log")
        anomalies = await agent.detect_anomalies(logs)
        
        assert len(anomalies) > 0
        assert anomalies[0].confidence >= 0.8
```

### Running Tests

```bash
# Unit tests (fast)
pytest tests/unit -v

# Integration tests
pytest tests/integration -v --run-integration

# E2E tests
pytest tests/e2e -v --run-e2e

# With coverage
pytest --cov=haci --cov-report=html --cov-fail-under=80

# Specific test file
pytest tests/unit/agents/test_log_analyst.py -v

# Specific test
pytest tests/unit/agents/test_log_analyst.py::TestLogAnalyst::test_log_parsing -v
```

## Documentation

### Documentation Structure

```
docs/
├── architecture/      # System design documentation
├── governance/        # Compliance and governance
├── integration/       # Integration guides
├── guides/            # How-to guides
└── api/               # API reference
```

### Documentation Standards

- Use Markdown for all documentation
- Include code examples where applicable
- Keep diagrams in ASCII art or Mermaid format for version control
- Update README.md table of contents when adding new docs

## Architecture Decision Records (ADRs)

For significant architectural decisions, create an ADR:

```
docs/architecture/adr/
├── 0001-use-harness-pattern.md
├── 0002-multi-provider-llm-strategy.md
└── template.md
```

Use the template in `docs/architecture/adr/template.md`.

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** with appropriate commits

3. **Ensure quality checks pass**
   ```bash
   # Run all checks
   pre-commit run --all-files
   pytest
   ```

4. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Fill out the PR template** completely

6. **Request review** from maintainers

7. **Address feedback** and update as needed

8. **Squash and merge** once approved

## Release Process

HACI follows [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

Releases are automated via GitHub Actions when a tag is pushed.

## Getting Help

- **Discord**: Join our [community server](https://discord.gg/your-org)
- **Discussions**: Use [GitHub Discussions](https://github.com/your-org/haci/discussions) for questions
- **Issues**: Report bugs via [GitHub Issues](https://github.com/your-org/haci/issues)

## Recognition

Contributors are recognized in:
- [CONTRIBUTORS.md](CONTRIBUTORS.md) — All contributors
- Release notes — Significant contributions highlighted

Thank you for contributing to HACI! 🎉
