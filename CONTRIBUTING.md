# Contributing to SOMAS

Thank you for your interest in contributing to SOMAS (Self-Sovereign Orchestrated Multi-Agent System). This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Development Setup](#development-setup)
- [Branch Naming Convention](#branch-naming-convention)
- [Testing Requirements](#testing-requirements)
- [Code Style](#code-style)
- [Pull Request Process](#pull-request-process)
- [Agent Development Guide](#agent-development-guide)
- [Docstring Format](#docstring-format)

---

## Code of Conduct

### Our Standards

- Be respectful and inclusive in all interactions
- Provide constructive feedback
- Focus on the work, not the person
- Accept responsibility for mistakes and learn from them
- Prioritize the project's best interests

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Personal attacks or trolling
- Publishing others' private information
- Other conduct inappropriate for a professional setting

Report violations to the project maintainers.

---

## Development Setup

### Prerequisites

- **Python**: 3.10 or higher
- **pip** or **poetry** for dependency management
- **Git** for version control
- **GitHub account** with repository access

### Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-org/somas.git
   cd somas
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Install pre-commit hooks** (optional but recommended):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

5. **Verify installation**:
   ```bash
   python -m pytest tests/ -v
   ```

### Environment Variables

Create a `.env` file for local development (never commit this file):

```bash
# .env.example (copy to .env)
GITHUB_TOKEN=your_github_token
AI_API_KEY=your_api_key
```

---

## Branch Naming Convention

Use descriptive branch names following this pattern:

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/<description>` | `feature/add-new-agent` |
| Bug fix | `fix/<description>` | `fix/state-manager-race-condition` |
| Documentation | `docs/<description>` | `docs/update-api-reference` |
| Refactor | `refactor/<description>` | `refactor/simplify-feedback-loop` |
| Test | `test/<description>` | `test/add-circuit-breaker-tests` |
| SOMAS pipeline | `somas/<project-id>` | `somas/project-123` |

**Guidelines**:
- Use lowercase letters and hyphens
- Keep names concise but descriptive
- Include issue number when applicable: `fix/123-validation-error`

---

## Testing Requirements

### Coverage Target

All code must maintain **80% or higher test coverage**. This is enforced in the CI pipeline.

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=somas --cov-report=html

# Run specific test file
pytest tests/test_state_manager.py -v

# Run specific test
pytest tests/test_state_manager.py::test_create_checkpoint -v
```

### Test Types

| Type | Location | Purpose |
|------|----------|---------|
| Unit tests | `tests/unit/` | Test individual functions/classes |
| Integration tests | `tests/integration/` | Test component interactions |
| End-to-end tests | `tests/e2e/` | Test complete workflows |

### Writing Tests

- Use `pytest` as the testing framework
- Use descriptive test names: `test_create_checkpoint_with_valid_data`
- Include both positive and negative test cases
- Mock external dependencies (API calls, file I/O)
- Test edge cases and error conditions

Example test structure:

```python
"""Tests for state manager functionality."""

import pytest
from somas.core.state_manager import StateManager


class TestStateManager:
    """Test suite for StateManager class."""

    def test_create_checkpoint_success(self):
        """Test creating a checkpoint with valid data."""
        manager = StateManager()
        checkpoint = manager.create_checkpoint("test-project", {"stage": "implementation"})

        assert checkpoint is not None
        assert checkpoint["project_id"] == "test-project"

    def test_create_checkpoint_invalid_project_id(self):
        """Test creating checkpoint with invalid project ID raises error."""
        manager = StateManager()

        with pytest.raises(ValueError):
            manager.create_checkpoint("", {"stage": "implementation"})
```

---

## Code Style

### Python Style Guidelines

SOMAS follows **PEP 8** with these additional requirements:

1. **Line length**: Maximum 100 characters
2. **Imports**: Group in order: standard library, third-party, local
3. **Type hints**: Required for all public functions
4. **Docstrings**: Required for all public modules, classes, and functions

### Type Hints

All public functions must include type hints:

```python
def process_stage(
    project_id: str,
    stage_name: str,
    options: Optional[Dict[str, Any]] = None
) -> StageResult:
    """Process a pipeline stage."""
    ...
```

### Linting

Run linting before committing:

```bash
# Format code with black
black somas/ tests/

# Check types with mypy
mypy somas/

# Lint with flake8
flake8 somas/ tests/
```

---

## Pull Request Process

### Before Submitting

1. **Create a branch** following the naming convention
2. **Write tests** for new functionality
3. **Run all tests** and ensure they pass
4. **Update documentation** if needed
5. **Run linting** and fix any issues

### PR Checklist

```markdown
- [ ] Tests added/updated and passing
- [ ] Code coverage maintained at 80%+
- [ ] Documentation updated
- [ ] Linting passes (black, flake8, mypy)
- [ ] Commit messages are clear and descriptive
- [ ] Branch is up to date with main
```

### Review Process

1. Submit PR against the `main` branch
2. Fill out the PR template completely
3. Request review from maintainers
4. Address review feedback
5. Await approval and merge

### Commit Messages

Use clear, descriptive commit messages:

```
<type>: <short description>

<optional longer description>

<optional footer with issue reference>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat: add circuit breaker for external API calls

Implements exponential backoff and failure threshold
to prevent cascading failures during API outages.

Closes #123
```

---

## Agent Development Guide

### Adding a New Agent

1. **Create agent configuration** in `.somas/agents/<agent-name>.yml`:

   ```yaml
   # .somas/agents/my-agent.yml
   role: "My Agent Role"
   provider: "claude_sonnet_4_5"

   instructions: |
     Your agent instructions here.
     Be specific about the task.

   output_format:
     - "Expected output 1"
     - "Expected output 2"

   quality_checks:
     - "Check 1"
     - "Check 2"
   ```

2. **Create agent instructions** in `.github/agents/somas-<agent-name>.md`

3. **Register agent** in `.somas/config.yml`:

   ```yaml
   agents:
     agent_configs:
       my_agent:
         provider: "claude_sonnet_4_5"
         fallback: "grok_code_fast_1"
         config_file: ".somas/agents/my-agent.yml"
         description: "Description of what this agent does"
   ```

4. **Add tests** for the new agent functionality

### Agent Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `role` | Yes | Short description of agent's role |
| `provider` | Yes | AI model provider to use |
| `instructions` | Yes | Detailed instructions for the agent |
| `output_format` | Yes | Expected output artifacts |
| `quality_checks` | No | Quality gates for agent output |
| `fallback` | No | Fallback provider if primary fails |

### Best Practices for Agents

- Keep instructions clear and specific
- Define measurable quality checks
- Include example inputs/outputs
- Document edge cases and error handling
- Test with various input scenarios

---

## Docstring Format

SOMAS uses **Google-style docstrings**:

### Module Docstring

```python
"""
Module description.

Extended description if needed.

Attributes:
    module_level_variable: Description of the variable.

Example:
    Usage example::

        from somas.core import module
        result = module.function()
"""
```

### Function Docstring

```python
def function_name(param1: str, param2: int, optional: Optional[str] = None) -> Dict[str, Any]:
    """
    Short description of the function.

    Extended description if needed. Explain what the function does,
    not how it does it.

    Args:
        param1: Description of param1.
        param2: Description of param2.
        optional: Description of optional parameter. Defaults to None.

    Returns:
        Description of return value.

    Raises:
        ValueError: When param1 is empty.
        TypeError: When param2 is not an integer.

    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        {'status': 'success'}
    """
```

### Class Docstring

```python
class ClassName:
    """
    Short description of the class.

    Extended description explaining the purpose and usage of the class.

    Attributes:
        attribute1: Description of attribute1.
        attribute2: Description of attribute2.

    Example:
        >>> obj = ClassName(param1="value")
        >>> obj.method()
    """

    def __init__(self, param1: str):
        """
        Initialize the class.

        Args:
            param1: Description of param1.
        """
```

---

## Questions and Support

- **Questions**: Open an issue with the `somas:question` label
- **Bugs**: Open an issue with the `somas:bug` label
- **Feature requests**: Open an issue with the `somas:enhance` label

Thank you for contributing to SOMAS!
