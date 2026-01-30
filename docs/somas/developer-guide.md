# SOMAS Developer Guide

This guide covers how to extend and modify the SOMAS autonomous pipeline.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Adding a New Agent](#adding-a-new-agent)
- [Adding a New Pipeline Stage](#adding-a-new-pipeline-stage)
- [Modifying APO](#modifying-apo)
- [State Management Patterns](#state-management-patterns)
- [Testing Patterns](#testing-patterns)
- [Debugging Tips](#debugging-tips)

---

## Architecture Overview

### High-Level Architecture

SOMAS follows a modular architecture with clear separation of concerns:

```
somas/
├── __init__.py          # Package entry point
├── core/                # Core orchestration
│   ├── state_manager.py # State persistence
│   ├── runner.py        # Pipeline execution
│   ├── feedback_loop.py # Iterative refinement
│   └── circuit_breaker.py # Fault tolerance
├── agents/              # Agent implementations
│   └── cost_tracker.py  # Usage tracking
├── analytics/           # Metrics and reporting
│   └── poc_metrics.py   # POC value tracking
└── apo/                 # Autonomous Prompt Optimization
```

### Configuration Architecture

```
.somas/
├── config.yml           # Main configuration
├── agents/              # Agent configurations (24 YAML files)
├── stages/              # Stage configurations
├── apo/                 # APO configurations
│   ├── mental-models.yml
│   ├── task-analyzer.yml
│   └── chains/
└── analytics/           # Analytics storage
    ├── schema.yml
    ├── runs/
    └── poc/
```

### Data Flow

```
Issue Created → Triage → Pipeline Stages → PR Created
                  ↓
            Orchestrator
                  ↓
         ┌───────┴───────┐
         ↓               ↓
    Stage Agents    State Manager
         ↓               ↓
      Outputs       Checkpoints
         ↓               ↓
    Quality Gates   Recovery Data
```

---

## Adding a New Agent

### Step 1: Create Agent Configuration

Create a YAML file in `.somas/agents/`:

```yaml
# .somas/agents/my-new-agent.yml
role: "My New Agent Role"
provider: "claude_sonnet_4_5"
fallback_provider: "grok_code_fast_1"

context: |
  @copilot-context: Description of when this agent is invoked
  @copilot-review: What this agent should validate

instructions: |
  You are the My New Agent for the SOMAS autonomous pipeline.

  Your responsibilities:
  1. [Responsibility 1]
  2. [Responsibility 2]
  3. [Responsibility 3]

  Guidelines:
  - Be specific and actionable
  - Document all decisions
  - Escalate when uncertain

input_artifacts:
  - "previous_stage_output.md"
  - "requirements.yml"

output_format:
  - "Primary output artifact"
  - "Secondary output (if applicable)"

output_artifacts:
  primary: "my_output.md"
  secondary: "my_data.json"

quality_checks:
  - "Output is complete and actionable"
  - "All requirements addressed"
  - "No ambiguous statements"

escalation_criteria:
  - "Unresolvable ambiguity"
  - "Missing critical information"
  - "Conflicting requirements"
```

### Step 2: Register Agent in Config

Add to `.somas/config.yml`:

```yaml
agents:
  agent_configs:
    my_new_agent:
      provider: "claude_sonnet_4_5"
      fallback: "grok_code_fast_1"
      config_file: ".somas/agents/my-new-agent.yml"
      description: "Description of what this agent does"
```

### Step 3: Create GitHub Copilot Instructions

Create `.github/agents/somas-my-new-agent.md`:

```markdown
# My New Agent Instructions

You are the My New Agent for SOMAS.

## Context
[When this agent is invoked and why]

## Inputs
- Previous stage artifacts
- Requirements specification

## Process
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Output
[Expected output format and location]

## Quality Criteria
- [Criterion 1]
- [Criterion 2]
```

### Step 4: Add APO Preferences (Optional)

If your agent benefits from specific mental models, add to `.somas/config.yml`:

```yaml
apo:
  mental_models:
    agent_preferences:
      my_new_agent:
        prefer: ["first_principles", "inversion"]
        avoid: ["tree_of_thoughts"]
```

### Step 5: Write Tests

Create `tests/test_my_new_agent.py`:

```python
"""Tests for my new agent."""

import pytest
from unittest.mock import Mock, patch


class TestMyNewAgent:
    """Test suite for My New Agent."""

    def test_agent_config_exists(self):
        """Verify agent configuration file exists."""
        import os
        assert os.path.exists(".somas/agents/my-new-agent.yml")

    def test_agent_registered_in_config(self):
        """Verify agent is registered in main config."""
        import yaml
        with open(".somas/config.yml") as f:
            config = yaml.safe_load(f)
        assert "my_new_agent" in config["agents"]["agent_configs"]
```

---

## Adding a New Pipeline Stage

### Step 1: Define Stage in Config

Add to `pipeline.stages` in `.somas/config.yml`:

```yaml
pipeline:
  stages:
    # ... existing stages ...

    - id: "my_new_stage"
      order: 12  # After existing stages
      code_name: "MYSTAGE"
      description: "My Stage - What it does"
      enabled: true
      agent: "my_new_agent"
      human_gate: false
      auto_proceed: true
      timeout_hours: 4
```

### Step 2: Create Stage Configuration

Create `.somas/stages/my_new_stage.yml`:

```yaml
my_new_stage:
  id: "my_new_stage"
  order: 12
  objective: "What this stage accomplishes"

  agents:
    primary: "my_new_agent"
    support: ["advisor"]

  inputs:
    required:
      - "previous_stage_output.md"
    optional:
      - "additional_context.json"

  outputs:
    - "my_stage_output.md"
    - "my_stage_data.json"

  quality_gates:
    - "Gate 1 description"
    - "Gate 2 description"

  human_gate: false
  auto_proceed: true
```

### Step 3: Add Quality Gates

Add to `quality_gates` in `.somas/config.yml`:

```yaml
quality_gates:
  my_new_stage:
    - "Quality gate 1"
    - "Quality gate 2"
    - "Quality gate 3"
```

### Step 4: Update Artifact Types

Add to `artifacts.types` in `.somas/config.yml`:

```yaml
artifacts:
  types:
    my_new_stage:
      - "my_stage_output.md"
      - "my_stage_data.json"
```

---

## Modifying APO

### Adding a Mental Model

1. Add to `.somas/apo/mental-models.yml`:

```yaml
models:
  my_new_model:
    name: "My New Model"
    description: "What this model does"
    when_to_use:
      - "Situation 1"
      - "Situation 2"
    process:
      - "Step 1"
      - "Step 2"
      - "Step 3"
    questions:
      - "Question to ask?"
      - "Another question?"
```

2. Enable in config:

```yaml
apo:
  mental_models:
    enabled_models:
      - "my_new_model"
```

### Modifying Complexity Thresholds

Adjust task analyzer in `.somas/config.yml`:

```yaml
apo:
  task_analyzer:
    complexity_thresholds:
      simple: 2.0      # Score < 2.0
      moderate: 3.5    # Score 2.0-3.5
      complex: 5.0     # Score 3.5-5.0
      # Score > 5.0 = novel

    auto_routing:
      rules:
        - complexity: "> 5.0"
          model: "claude_opus_4_5"
          chain: "strategic_diamond"
```

### Adding a Chain Strategy

Create `.somas/apo/chains/my-chain.yml`:

```yaml
name: "my_chain"
description: "Description of this chain"

steps:
  - name: "step_1"
    action: "Initial analysis"
    output: "analysis_result"

  - name: "step_2"
    action: "Process analysis"
    input: "analysis_result"
    output: "processed_result"

  - name: "step_3"
    action: "Final synthesis"
    input: "processed_result"
    output: "final_output"
```

---

## State Management Patterns

### Creating Checkpoints

```python
from somas.core.state_manager import StateManager

def process_with_checkpoints(project_id: str, data: dict):
    """Process data with checkpoint recovery."""
    manager = StateManager(project_id=project_id)

    # Create checkpoint before risky operation
    checkpoint = manager.create_checkpoint(
        stage="implementation",
        data={"status": "starting", "input": data}
    )

    try:
        result = perform_risky_operation(data)

        # Update checkpoint on success
        manager.update_checkpoint(
            checkpoint_id=checkpoint["id"],
            data={"status": "completed", "result": result}
        )

        return result

    except Exception as e:
        # Record failure for dead letter recovery
        manager.record_dead_letter(
            checkpoint_id=checkpoint["id"],
            error=str(e),
            context={"data": data}
        )
        raise
```

### Recovering from Failures

```python
def resume_from_failure(project_id: str):
    """Resume processing from last checkpoint."""
    manager = StateManager(project_id=project_id)

    # Get recovery information
    state = manager.get_current_state()

    if state.get("recovery_info", {}).get("can_resume"):
        checkpoint = manager.get_checkpoint(
            state["recovery_info"]["last_successful_checkpoint"]
        )

        # Resume from checkpoint data
        return resume_processing(checkpoint["data"])

    return None
```

### State Transition Logging

```python
def log_transition(project_id: str, from_stage: str, to_stage: str):
    """Log state transition for audit trail."""
    manager = StateManager(project_id=project_id)

    manager.log_transition({
        "from_stage": from_stage,
        "to_stage": to_stage,
        "timestamp": datetime.utcnow().isoformat(),
        "reason": "Stage completed successfully"
    })
```

---

## Testing Patterns

### Unit Test Structure

Reference implementation: `tests/test_state_manager.py`

```python
"""Tests for state manager functionality."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from somas.core.state_manager import StateManager


class TestStateManager:
    """Test suite for StateManager."""

    @pytest.fixture
    def manager(self):
        """Create StateManager instance for testing."""
        return StateManager(project_id="test-project")

    def test_create_checkpoint_success(self, manager):
        """Test checkpoint creation with valid data."""
        checkpoint = manager.create_checkpoint(
            stage="implementation",
            data={"files": ["main.py"]}
        )

        assert checkpoint is not None
        assert "id" in checkpoint
        assert checkpoint["stage"] == "implementation"

    def test_create_checkpoint_invalid_stage(self, manager):
        """Test checkpoint creation with invalid stage."""
        with pytest.raises(ValueError):
            manager.create_checkpoint(stage="", data={})


class TestStateManagerWithMocks:
    """Tests using mocks for external dependencies."""

    @patch("somas.core.state_manager.filelock.FileLock")
    def test_concurrent_access(self, mock_lock):
        """Test file locking during concurrent access."""
        mock_lock.return_value.__enter__ = Mock()
        mock_lock.return_value.__exit__ = Mock()

        manager = StateManager(project_id="test")
        manager.create_checkpoint("test", {})

        mock_lock.assert_called()
```

### Integration Test Pattern

```python
"""Integration tests for pipeline stages."""

import pytest
import tempfile
import shutil


class TestPipelineIntegration:
    """Integration tests for full pipeline."""

    @pytest.fixture
    def temp_project_dir(self):
        """Create temporary project directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_stage_handoff(self, temp_project_dir):
        """Test data handoff between stages."""
        # Setup stage 1 output
        stage1_output = {"requirements": ["REQ-001"]}

        # Run stage 2 with stage 1 output
        stage2_result = run_stage(
            stage="specification",
            input_data=stage1_output,
            project_dir=temp_project_dir
        )

        assert stage2_result is not None
        assert "spec" in stage2_result
```

### Mocking External APIs

```python
@pytest.fixture
def mock_ai_response():
    """Mock AI API responses."""
    with patch("somas.agents.api_client.call_model") as mock:
        mock.return_value = {
            "content": "Mocked response",
            "tokens": 100,
            "success": True
        }
        yield mock
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=somas --cov-report=html

# Run specific test file
pytest tests/test_state_manager.py -v

# Run tests matching pattern
pytest tests/ -k "checkpoint" -v

# Run with verbose output
pytest tests/ -v --tb=long
```

---

## Debugging Tips

### Enable Debug Logging

In `.somas/config.yml`:

```yaml
development:
  debug_mode: true
  verbose_logging: true
  save_intermediate_states: true
```

### Check State Files

```bash
# View current state
cat .somas/projects/<project-id>/state.json | jq .

# View recent transitions
tail -20 .somas/projects/<project-id>/transitions.jsonl

# Check dead letters
cat .somas/projects/<project-id>/dead_letters.json | jq .
```

### Common Issues

#### Agent Not Responding

1. Check agent configuration exists
2. Verify provider is available
3. Check API key is set
4. Review timeout settings

#### State Recovery Failing

1. Check `state.json` is valid JSON
2. Verify checkpoint exists
3. Check file permissions
4. Review `dead_letters.json` for context

#### Quality Gate Failures

1. Review specific gate that failed
2. Check agent output against criteria
3. Verify input artifacts are complete
4. Check for ambiguous requirements

### Debug Commands

```bash
# Validate configuration
python -c "import yaml; yaml.safe_load(open('.somas/config.yml'))"

# Check agent configs
for f in .somas/agents/*.yml; do
  python -c "import yaml; yaml.safe_load(open('$f'))" && echo "$f: OK"
done

# List all project states
ls -la .somas/projects/*/state.json
```

### Logging Best Practices

```python
import logging

logger = logging.getLogger(__name__)

def process_stage(project_id: str, stage: str):
    """Process a pipeline stage with proper logging."""
    logger.info(f"Starting stage {stage} for project {project_id}")

    try:
        result = do_work()
        logger.info(f"Stage {stage} completed successfully")
        logger.debug(f"Stage result: {result}")
        return result

    except Exception as e:
        logger.error(f"Stage {stage} failed: {e}", exc_info=True)
        raise
```

---

## See Also

- [Configuration Reference](configuration-reference.md) - All config options
- [Test Strategy](test-strategy.md) - Testing approach
- [Architecture Diagrams](architecture-diagrams.md) - Visual architecture
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues
