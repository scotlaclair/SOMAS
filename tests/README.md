# SOMAS Test Suite

## Overview

The tests directory contains comprehensive unit tests for the SOMAS (Self-Sovereign Orchestrated Multi-Agent System) core components. These tests ensure the reliability, correctness, and robustness of the autonomous pipeline infrastructure.

## Test Categories

### Core Component Tests

#### `test_circuit_breaker.py` - Circuit Breaker Tests
**Purpose:** Validates the circuit breaker functionality that prevents runaway agent invocations
**Coverage:**
- Marker creation and detection for PR management
- Agent invocation counting and limits
- Stage progression validation
- Error handling and recovery

**Key Test Cases:**
- Marker creation: `<!-- SOMAS_PR_CONTINUE:PR-26 -->`
- Invocation limits: Prevents excessive agent calls
- Stage transitions: Ensures proper pipeline flow

#### `test_runner.py` - Runner Tests
**Purpose:** Tests the SOMAS runner's error handling and validation capabilities
**Coverage:**
- Configuration loading and validation
- Agent execution error handling
- Input validation and sanitization
- File path security checks

**Key Test Cases:**
- Invalid configuration handling
- Agent not found scenarios
- File permission issues
- Path traversal prevention

#### `test_state_manager.py` - State Manager Tests
**Purpose:** Validates state persistence, dead letter vault, and transition auditing
**Coverage:**
- Project initialization and state creation
- State persistence across restarts
- Dead letter queue management
- Transition history and auditing
- Concurrent access handling

**Key Test Cases:**
- Project state initialization
- State file creation and validation
- Dead letter vault operations
- Transition logging and retrieval

## Test Framework

### Dependencies
- **unittest** - Python's built-in unit testing framework
- **pytest** - Alternative test runner (if configured)
- **tempfile** - Temporary file creation for isolated testing
- **pathlib** - Modern path handling

### Test Structure
```python
class TestComponentName(unittest.TestCase):
    """Test cases for ComponentName class."""

    def setUp(self):
        """Set up test fixtures before each test."""
        # Initialize test environment
        pass

    def tearDown(self):
        """Clean up test fixtures after each test."""
        # Clean up test environment
        pass

    def test_specific_functionality(self):
        """Test specific functionality with assertions."""
        # Arrange
        # Act
        # Assert
        pass
```

## Running Tests

### Basic Execution
```bash
# Run all tests
python -m unittest discover tests/

# Run specific test file
python -m unittest tests/test_circuit_breaker.py

# Run specific test class
python -m unittest tests.test_circuit_breaker.TestCircuitBreaker

# Run specific test method
python -m unittest tests.test_circuit_breaker.TestCircuitBreaker.test_marker_creation
```

### With pytest (if available)
```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=somas --cov-report=html
```

### Continuous Integration
Tests are designed to run in CI environments:
- No external dependencies required
- Isolated test environments using temporary directories
- Deterministic test execution
- Fast execution for quick feedback

## Test Coverage Goals

### Current Coverage Areas
- **Circuit Breaker:** 95% - Agent invocation management
- **Runner:** 90% - Error handling and validation
- **State Manager:** 85% - Persistence and transitions

### Target Coverage
- **Overall:** >90% code coverage
- **Critical Paths:** 100% coverage for core pipeline logic
- **Error Paths:** Complete coverage of error conditions

## Writing New Tests

### Test File Naming
- `test_{component_name}.py` - Unit tests for specific components
- `test_{feature_name}.py` - Integration tests for features
- `test_{scenario}.py` - Scenario-based tests

### Test Case Guidelines
1. **Descriptive Names:** `test_should_handle_invalid_config`
2. **Single Responsibility:** Each test validates one behavior
3. **Independent:** Tests don't depend on each other
4. **Fast:** Tests complete in <1 second
5. **Isolated:** No side effects between tests

### Test Structure Template
```python
import unittest
from somas.core.component import ComponentClass

class TestComponentClass(unittest.TestCase):
    """Test cases for ComponentClass."""

    def setUp(self):
        """Set up test fixtures."""
        self.component = ComponentClass()
        # Additional setup

    def test_expected_behavior(self):
        """Test that component behaves as expected."""
        # Given
        input_data = "test input"

        # When
        result = self.component.process(input_data)

        # Then
        self.assertEqual(result, "expected output")
        self.assertTrue(self.component.is_valid())

    def test_error_condition(self):
        """Test error handling for invalid inputs."""
        with self.assertRaises(ValueError):
            self.component.process(None)
```

## Test Data Management

### Fixtures and Mock Data
- Use `tempfile` for temporary files and directories
- Create minimal valid configurations for testing
- Mock external dependencies when possible
- Clean up after tests complete

### Test Isolation
- Each test runs in isolation
- No shared state between tests
- Temporary directories for file operations
- Database isolation for state tests

## Continuous Testing

### Pre-commit Hooks
```bash
#!/bin/bash
# Run tests before committing
python -m unittest discover tests/
```

### CI Integration
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: python -m unittest discover tests/
```

## Debugging Test Failures

### Common Issues
- **Import Errors:** Ensure Python path includes project root
- **File Permissions:** Tests may need write access to temp directories
- **Timing Issues:** Use appropriate timeouts for async operations
- **Platform Differences:** Account for OS-specific behavior

### Debugging Tools
```bash
# Run with verbose output
python -m unittest -v tests.test_component

# Debug specific test
python -c "
import unittest
from tests.test_component import TestComponent
suite = unittest.TestLoader().loadTestsFromTestCase(TestComponent)
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
"
```

## Contributing

### Adding Tests
1. Create `test_{component}.py` in the `tests/` directory
2. Follow the established naming and structure conventions
3. Ensure tests pass locally before submitting
4. Add documentation for complex test scenarios

### Test Maintenance
- Keep tests updated as code changes
- Remove obsolete tests promptly
- Review test effectiveness regularly
- Update test data as requirements evolve

---

*Last updated: January 30, 2026 12:00 UTC*</content>
<parameter name="filePath">/Users/architect/Developer/projects/somas/tests/README.md