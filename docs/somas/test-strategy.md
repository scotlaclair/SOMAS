# SOMAS Test Strategy

This document describes the testing philosophy, coverage targets, and testing patterns for the SOMAS autonomous pipeline.

## Table of Contents

- [Testing Philosophy](#testing-philosophy)
- [Coverage Targets](#coverage-targets)
- [Test Types](#test-types)
- [Current Coverage Status](#current-coverage-status)
- [Testing Patterns](#testing-patterns)
- [Running Tests](#running-tests)
- [CI/CD Integration](#cicd-integration)

---

## Testing Philosophy

### Core Principles

1. **Quality over Quantity**: Meaningful tests that catch real bugs, not just line coverage
2. **Test Behavior, Not Implementation**: Focus on what code does, not how it does it
3. **Fast Feedback**: Tests should run quickly to enable rapid iteration
4. **Isolation**: Tests should not depend on external services or other tests
5. **Readability**: Tests serve as documentation for expected behavior

### Test Pyramid

```
         ╱╲
        ╱  ╲
       ╱ E2E╲         Few: Complete workflow tests
      ╱──────╲
     ╱        ╲
    ╱Integration╲     Some: Component interaction tests
   ╱──────────────╲
  ╱                ╲
 ╱   Unit Tests     ╲  Many: Individual function/class tests
╱────────────────────╲
```

### Testing by Layer

| Layer | Focus | Examples |
|-------|-------|----------|
| Unit | Individual functions/classes | State manager, feedback loop |
| Integration | Component interactions | Agent handoffs, state persistence |
| E2E | Complete workflows | Full pipeline execution |

---

## Coverage Targets

### Required Coverage

| Module | Minimum | Target |
|--------|---------|--------|
| `somas/core/` | 80% | 90% |
| `somas/agents/` | 80% | 85% |
| `somas/analytics/` | 80% | 85% |
| `somas/apo/` | 75% | 85% |
| **Overall** | **80%** | **85%** |

### Coverage Enforcement

Coverage is enforced in CI/CD. Pull requests with coverage below 80% will fail.

### Measuring Coverage

```bash
# Generate coverage report
pytest tests/ -v --cov=somas --cov-report=html --cov-report=term-missing

# View HTML report
open htmlcov/index.html
```

---

## Test Types

### Unit Tests

**Purpose**: Test individual functions and classes in isolation.

**Location**: `tests/unit/`

**Characteristics**:
- Fast execution (< 1 second per test)
- No external dependencies (mocked)
- Test single behavior per test
- Use descriptive test names

**Example**:

```python
"""Unit tests for state manager."""

import pytest
from somas.core.state_manager import StateManager


class TestStateManagerCheckpoints:
    """Tests for checkpoint functionality."""

    def test_create_checkpoint_returns_id(self):
        """Creating a checkpoint returns a unique ID."""
        manager = StateManager(project_id="test")
        checkpoint = manager.create_checkpoint("stage", {"data": "value"})

        assert checkpoint["id"] is not None
        assert len(checkpoint["id"]) > 0

    def test_create_checkpoint_stores_stage(self):
        """Checkpoint stores the stage name."""
        manager = StateManager(project_id="test")
        checkpoint = manager.create_checkpoint("implementation", {})

        assert checkpoint["stage"] == "implementation"

    def test_create_checkpoint_with_empty_project_id_raises(self):
        """Empty project ID raises ValueError."""
        with pytest.raises(ValueError, match="project_id"):
            StateManager(project_id="")
```

### Integration Tests

**Purpose**: Test component interactions and data flow.

**Location**: `tests/integration/`

**Characteristics**:
- Test multiple components together
- May use real file system (temp directories)
- Test data flows and handoffs
- Slower than unit tests (< 10 seconds)

**Example**:

```python
"""Integration tests for stage handoffs."""

import pytest
import tempfile
import os


class TestStageHandoff:
    """Tests for data handoff between pipeline stages."""

    @pytest.fixture
    def temp_project(self):
        """Create temporary project structure."""
        temp_dir = tempfile.mkdtemp()
        os.makedirs(f"{temp_dir}/.somas/projects/test-123/artifacts")
        yield temp_dir
        import shutil
        shutil.rmtree(temp_dir)

    def test_specification_output_available_for_simulation(self, temp_project):
        """Specification output is accessible to simulation stage."""
        # Write specification output
        spec_path = f"{temp_project}/.somas/projects/test-123/artifacts/SPEC.md"
        with open(spec_path, "w") as f:
            f.write("# Specification\n\nRequirements here.")

        # Verify simulation can read it
        assert os.path.exists(spec_path)
        with open(spec_path) as f:
            content = f.read()
        assert "Specification" in content
```

### End-to-End Tests

**Purpose**: Test complete workflows from start to finish.

**Location**: `tests/e2e/`

**Characteristics**:
- Test full pipeline scenarios
- May use mock AI responses
- Verify end-to-end behavior
- Slowest tests (< 60 seconds)

**Example**:

```python
"""End-to-end tests for pipeline execution."""

import pytest
from unittest.mock import patch, Mock


class TestPipelineE2E:
    """End-to-end pipeline tests."""

    @pytest.fixture
    def mock_ai_responses(self):
        """Mock all AI API calls."""
        with patch("somas.agents.api_client.call_model") as mock:
            mock.return_value = {
                "content": "Mock response",
                "success": True
            }
            yield mock

    def test_simple_project_completes(self, mock_ai_responses):
        """Simple project completes all stages successfully."""
        from somas.core.runner import PipelineRunner

        runner = PipelineRunner(project_id="e2e-test")
        result = runner.execute_pipeline({
            "title": "Simple CLI Tool",
            "description": "A command-line tool"
        })

        assert result["status"] == "completed"
        assert all(s["status"] == "completed" for s in result["stages"])
```

---

## Current Coverage Status

### Coverage by Module

| Module | Lines | Covered | Coverage |
|--------|-------|---------|----------|
| `somas/core/state_manager.py` | 150 | 135 | 90% |
| `somas/core/feedback_loop.py` | 120 | 96 | 80% |
| `somas/core/runner.py` | 200 | 160 | 80% |
| `somas/agents/cost_tracker.py` | 50 | 40 | 80% |
| `somas/analytics/poc_metrics.py` | 100 | 85 | 85% |
| **Total** | **620** | **516** | **83%** |

### Areas Needing Improvement

1. Error handling paths in `runner.py`
2. Edge cases in `feedback_loop.py`
3. Recovery scenarios in `state_manager.py`

---

## Testing Patterns

### Mocking External Dependencies

```python
from unittest.mock import patch, Mock, MagicMock


class TestWithMocks:
    """Tests using mock objects."""

    @patch("somas.core.state_manager.filelock.FileLock")
    def test_file_locking(self, mock_lock):
        """Test that file operations use locking."""
        mock_lock_instance = MagicMock()
        mock_lock.return_value = mock_lock_instance

        manager = StateManager(project_id="test")
        manager.create_checkpoint("stage", {})

        mock_lock.assert_called_once()
        mock_lock_instance.__enter__.assert_called()
```

### Using Fixtures

```python
import pytest


@pytest.fixture
def sample_project_data():
    """Sample project data for tests."""
    return {
        "id": "test-project-123",
        "title": "Test Project",
        "stages": ["specification", "implementation"],
        "status": "in_progress"
    }


@pytest.fixture
def state_manager(tmp_path):
    """State manager with temporary storage."""
    return StateManager(
        project_id="test",
        storage_path=str(tmp_path)
    )


class TestWithFixtures:
    """Tests using fixtures."""

    def test_project_creation(self, sample_project_data):
        """Test project creation with sample data."""
        assert sample_project_data["id"] == "test-project-123"

    def test_checkpoint_storage(self, state_manager):
        """Test checkpoint uses temp storage."""
        checkpoint = state_manager.create_checkpoint("test", {})
        assert checkpoint is not None
```

### Testing Async Code

```python
import pytest
import asyncio


class TestAsyncOperations:
    """Tests for async functionality."""

    @pytest.mark.asyncio
    async def test_async_stage_execution(self):
        """Test async stage execution."""
        from somas.core.runner import AsyncRunner

        runner = AsyncRunner(project_id="async-test")
        result = await runner.execute_stage_async("specification")

        assert result["status"] == "completed"

    @pytest.mark.asyncio
    async def test_concurrent_operations(self):
        """Test concurrent checkpoint operations."""
        tasks = [
            create_checkpoint_async(f"project-{i}")
            for i in range(5)
        ]

        results = await asyncio.gather(*tasks)
        assert all(r["success"] for r in results)
```

### Testing Error Conditions

```python
class TestErrorHandling:
    """Tests for error handling."""

    def test_invalid_input_raises_value_error(self):
        """Invalid input raises ValueError with message."""
        manager = StateManager(project_id="test")

        with pytest.raises(ValueError) as exc_info:
            manager.create_checkpoint("", {})

        assert "stage" in str(exc_info.value).lower()

    def test_missing_file_returns_none(self):
        """Missing checkpoint file returns None, not error."""
        manager = StateManager(project_id="test")

        result = manager.get_checkpoint("nonexistent-id")

        assert result is None

    def test_corrupted_state_triggers_recovery(self):
        """Corrupted state file triggers recovery process."""
        manager = StateManager(project_id="test")
        # Write corrupted JSON
        manager._write_state("not valid json {{{")

        # Should trigger recovery, not crash
        state = manager.get_current_state()
        assert state.get("recovered", False) or state == {}
```

### Parameterized Tests

```python
import pytest


class TestParameterized:
    """Tests with multiple parameter sets."""

    @pytest.mark.parametrize("stage,expected_agent", [
        ("signal", "planner"),
        ("design", "specifier"),
        ("grid", "simulator"),
        ("line", "decomposer"),
        ("mcp", "coder"),
        ("pulse", "validator"),
    ])
    def test_stage_agent_mapping(self, stage, expected_agent):
        """Each stage maps to correct agent."""
        from somas.core.config import get_stage_agent

        agent = get_stage_agent(stage)
        assert agent == expected_agent

    @pytest.mark.parametrize("complexity,expected_model", [
        (1.0, "grok_code_fast_1"),
        (2.5, "claude_sonnet_4_5"),
        (4.0, "claude_opus_4_5"),
    ])
    def test_complexity_routing(self, complexity, expected_model):
        """Task complexity routes to appropriate model."""
        from somas.apo.task_analyzer import get_model_for_complexity

        model = get_model_for_complexity(complexity)
        assert model == expected_model
```

---

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=somas --cov-report=html

# Run specific file
pytest tests/test_state_manager.py -v

# Run specific test
pytest tests/test_state_manager.py::TestStateManager::test_create_checkpoint -v

# Run tests matching pattern
pytest tests/ -k "checkpoint" -v

# Run only unit tests
pytest tests/unit/ -v

# Run only integration tests
pytest tests/integration/ -v
```

### Test Options

| Option | Description |
|--------|-------------|
| `-v` | Verbose output |
| `-vv` | More verbose output |
| `--tb=short` | Short traceback |
| `--tb=long` | Full traceback |
| `-x` | Stop on first failure |
| `--lf` | Run last failed tests |
| `-n auto` | Run in parallel (requires pytest-xdist) |

### Coverage Options

```bash
# HTML report
pytest --cov=somas --cov-report=html

# Terminal report with missing lines
pytest --cov=somas --cov-report=term-missing

# XML report for CI
pytest --cov=somas --cov-report=xml

# Fail if coverage below threshold
pytest --cov=somas --cov-fail-under=80
```

---

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run tests with coverage
        run: |
          pytest tests/ -v --cov=somas --cov-report=xml --cov-fail-under=80

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest tests/unit/ -v --tb=short
        language: system
        pass_filenames: false
        always_run: true
```

### Required Checks

| Check | Requirement |
|-------|-------------|
| Unit tests | All must pass |
| Integration tests | All must pass |
| Coverage | >= 80% |
| Lint | No errors |
| Type check | No errors |

---

## See Also

- [Developer Guide](developer-guide.md) - Development practices
- [CONTRIBUTING.md](../../CONTRIBUTING.md) - Contribution guidelines
- [pytest documentation](https://docs.pytest.org/) - Testing framework
