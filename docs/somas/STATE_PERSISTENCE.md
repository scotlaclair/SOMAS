# SOMAS State Persistence System

## Overview

The SOMAS State Persistence System provides robust JSON-based state management for the autonomous pipeline, enabling:

- **State Tracking**: Complete pipeline state in `state.json`
- **Fault Recovery**: Failed contexts in `dead_letters.json`
- **Audit Trail**: Chronological transitions in `transitions.jsonl`
- **Concurrent Safety**: File-based locking to prevent race conditions

This system is modeled after MathProtocol's "Dead Letter Vault" and MerkleAuditChain for high-assurance autonomous environments.

## Concurrency Safety

### File Locking Strategy

The StateManager uses file-based locking (`filelock` library) to ensure safe concurrent access:

**Lock Acquisition**: All read-modify-write operations acquire an exclusive lock on the target file before reading, modifying, or writing state.

**Timeout Behavior**: Lock operations timeout after 30 seconds if the lock cannot be acquired. This prevents indefinite blocking while still allowing concurrent operations to complete.

**Lock Files**: Lock files (`.lock` suffix) are automatically created and cleaned up. They are transient and should not be committed to version control.

**Multi-File Coordination**: Operations that modify multiple files (e.g., `add_dead_letter` modifying both `state.json` and `dead_letters.json`) acquire locks in a consistent order to prevent deadlocks.

### Methods Using File Locking

| Method | Lock Scope | Description |
|--------|-----------|-------------|
| `_atomic_write_json()` | Single file | Low-level write with atomic replacement |
| `_append_jsonl()` | Single file | Append-only log writes |
| `update_state()` | state.json | General state updates |
| `start_stage()` | state.json | Stage transition to in_progress |
| `complete_stage()` | state.json | Stage transition to completed |
| `fail_stage()` | state.json | Stage transition to failed |
| `create_checkpoint()` | state.json | Add recovery checkpoint |
| `add_dead_letter()` | state.json + dead_letters.json | Coordinated multi-file update |

### Lock Guarantees

**Atomicity**: All read-modify-write cycles execute atomically under a lock, preventing lost updates.

**Consistency**: Multi-file operations maintain consistency by acquiring all necessary locks before modifications.

**Isolation**: Concurrent operations on the same project are serialized, preventing race conditions.

**No Deadlocks**: Locks are acquired in a consistent order and held for minimal duration.

### Performance Considerations

**Lock Contention**: Under normal operation, lock contention is negligible. The 30-second timeout provides ample time for operations to complete.

**Scalability**: File locking is appropriate for the expected concurrency levels (typically 1-10 concurrent operations per project).

**Lock-Free Reads**: The `get_state()` method does not acquire locks, allowing concurrent reads. However, readers may see stale data during concurrent writes.

## Architecture

### File Structure

Each project has three persistent state files in `.somas/projects/{project_id}/`:

```
.somas/projects/project-123/
├── state.json           # Current pipeline state
├── state.json.lock      # Lock file (transient)
├── dead_letters.json    # Failed execution contexts
├── dead_letters.json.lock  # Lock file (transient)
└── transitions.jsonl    # Audit log (JSON Lines)
    └── transitions.jsonl.lock  # Lock file (transient)
```

### State Files

#### 1. `state.json` - Pipeline State

Complete snapshot of project state including:

- **Project metadata**: ID, issue number, branch, timestamps
- **Current stage**: Which pipeline stage is active
- **Stage statuses**: Status of each stage (pending/in_progress/completed/failed)
- **Checkpoints**: Recovery points with artifacts
- **Labels**: GitHub labels and custom metadata
- **Metrics**: Execution times, retry counts, artifact counts
- **Recovery info**: Last successful checkpoint, resume capability

**Example:**
```json
{
  "project_id": "project-123",
  "version": "1.0.0",
  "created_at": "2026-01-26T21:00:00Z",
  "updated_at": "2026-01-26T21:30:00Z",
  "issue_number": 123,
  "branch": "somas/project-123",
  "current_stage": "implementation",
  "status": "in_progress",
  "stages": {
    "ideation": {
      "status": "completed",
      "started_at": "2026-01-26T21:00:00Z",
      "completed_at": "2026-01-26T21:05:00Z",
      "duration_seconds": 300,
      "agent": "planner",
      "retry_count": 0,
      "artifacts": ["artifacts/initial_plan.md"]
    },
    "implementation": {
      "status": "in_progress",
      "started_at": "2026-01-26T21:25:00Z",
      "agent": "coder",
      "retry_count": 0
    }
  },
  "checkpoints": [
    {
      "id": "chk-abc123",
      "stage": "ideation",
      "timestamp": "2026-01-26T21:05:00Z",
      "status": "success",
      "artifacts": ["artifacts/initial_plan.md"]
    }
  ],
  "metrics": {
    "total_duration_seconds": 1800,
    "stage_durations": {
      "ideation": 300
    },
    "retry_count": 0,
    "agent_invocations": 2,
    "artifacts_generated": 1,
    "dead_letters": 0
  },
  "recovery_info": {
    "last_successful_checkpoint": "chk-abc123",
    "can_resume": true,
    "resume_from_stage": "implementation"
  }
}
```

#### 2. `dead_letters.json` - Failed Execution Contexts

Records every failure with full context for forensics, replay, and recovery:

- **Error details**: Type, message, stack trace
- **Execution context**: Inputs, environment, state snapshot
- **Request information**: Task details, parameters, timeout
- **Execution trace**: Breadcrumbs leading to failure
- **Recovery status**: Whether recovery was attempted and outcome

**Example:**
```json
{
  "project_id": "project-123",
  "version": "1.0.0",
  "entries": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "timestamp": "2026-01-26T21:15:00Z",
      "stage": "validation",
      "agent": "validator",
      "attempt_number": 2,
      "error": {
        "type": "TestFailureError",
        "message": "3 tests failed in test suite",
        "exit_code": 1
      },
      "context": {
        "inputs": {
          "test_suite": "integration_tests"
        },
        "environment": {
          "NODE_ENV": "test",
          "CI": "true"
        },
        "artifacts": [
          "src/api.js",
          "tests/api.test.js"
        ],
        "state_snapshot": {
          "current_stage": "validation",
          "status": "in_progress"
        }
      },
      "request": {
        "task": "Run validation tests",
        "parameters": {
          "test_command": "npm test"
        },
        "timeout_seconds": 300
      },
      "trace": [
        {
          "timestamp": "2026-01-26T21:14:30Z",
          "event": "test_suite_started",
          "details": {"suite": "integration_tests"}
        },
        {
          "timestamp": "2026-01-26T21:14:55Z",
          "event": "tests_failed",
          "details": {"failed_count": 3}
        }
      ],
      "labels": {
        "github": ["somas-project", "somas:validation"],
        "custom": {"priority": "high"}
      },
      "recovery_attempted": true,
      "recovery_result": "success",
      "replay_count": 1
    }
  ],
  "statistics": {
    "total_entries": 1,
    "by_stage": {
      "validation": 1
    },
    "by_agent": {
      "validator": 1
    },
    "recovered": 1,
    "unrecovered": 0
  }
}
```

#### 3. `transitions.jsonl` - Audit Log

Append-only log of all state transitions in JSON Lines format (one JSON object per line):

**Example entries:**
```jsonl
{"id":"trans-001","timestamp":"2026-01-26T21:00:00Z","project_id":"project-123","event_type":"project_initialized","metadata":{"issue_number":123,"title":"Build REST API"}}
{"id":"trans-002","timestamp":"2026-01-26T21:00:05Z","project_id":"project-123","event_type":"stage_started","stage":"ideation","agent":"planner"}
{"id":"trans-003","timestamp":"2026-01-26T21:05:00Z","project_id":"project-123","event_type":"stage_completed","stage":"ideation","metadata":{"completed_at":"2026-01-26T21:05:00Z","duration_seconds":300},"checkpoint_id":"chk-abc123"}
{"id":"trans-004","timestamp":"2026-01-26T21:15:00Z","project_id":"project-123","event_type":"error_recorded","stage":"validation","agent":"validator","error":{"type":"TestFailureError","message":"3 tests failed","dead_letter_id":"550e8400-e29b-41d4-a716-446655440000"}}
```

## State Manager API

### Python API

The `StateManager` class provides the programmatic interface:

```python
from somas.core.state_manager import StateManager

# Initialize
state_manager = StateManager()

# Initialize new project
state = state_manager.initialize_project(
    project_id="project-123",
    issue_number=123,
    title="Build REST API",
    branch="somas/project-123",
    labels=["somas-project"]
)

# Start a stage
state_manager.start_stage(
    project_id="project-123",
    stage="implementation",
    agent="coder"
)

# Complete a stage
state_manager.complete_stage(
    project_id="project-123",
    stage="implementation",
    artifacts=["src/api.js", "tests/api.test.js"],
    create_checkpoint=True
)

# Record a failure
state_manager.fail_stage(
    project_id="project-123",
    stage="validation",
    agent="validator",
    error={
        "type": "TestFailureError",
        "message": "3 tests failed"
    },
    context={
        "test_suite": "integration_tests"
    }
)

# Query state
state = state_manager.get_state("project-123")
transitions = state_manager.get_transitions("project-123", limit=10)
dead_letters = state_manager.get_dead_letters("project-123", unrecovered_only=True)
```

### CLI Integration

The agent runner integrates state management automatically:

```bash
python somas/core/runner.py \
  --agent coder \
  --task_name "API-Implementation" \
  --task_desc "Implement REST endpoints" \
  --context_files "SPEC.md,ARCH.md" \
  --output_path "artifacts/result.md" \
  --project_id "project-123" \
  --stage "implementation"
```

## Recovery and Replay

### Automatic Recovery

The system enables automatic recovery from failures:

1. **Checkpoint-based Resume**: Resume from last successful checkpoint
2. **Dead Letter Replay**: Replay failed operations with context
3. **State Reconciliation**: Verify state consistency on resume

### Manual Recovery

To manually recover a failed project:

```python
from somas.core.state_manager import StateManager

state_manager = StateManager()

# Get project state
state = state_manager.get_state("project-123")

# Check recovery info
recovery = state["recovery_info"]
if recovery["can_resume"]:
    resume_stage = recovery["resume_from_stage"]
    checkpoint = recovery["last_successful_checkpoint"]
    print(f"Can resume from {resume_stage} using checkpoint {checkpoint}")

# Get unrecovered failures
failures = state_manager.get_dead_letters("project-123", unrecovered_only=True)
for failure in failures:
    print(f"Failure in {failure['stage']}: {failure['error']['message']}")
    # Replay or fix as needed
```

## Forensics and Analytics

### Audit Trail Analysis

Query the transition log for forensics:

```python
# Get all transitions for a stage
transitions = state_manager.get_transitions(
    project_id="project-123",
    stage="validation"
)

# Get failures
failures = state_manager.get_transitions(
    project_id="project-123",
    event_type="stage_failed"
)
```

### Metrics and Analytics

Extract metrics from state:

```python
state = state_manager.get_state("project-123")

# Overall metrics
metrics = state["metrics"]
print(f"Total duration: {metrics['total_duration_seconds']}s")
print(f"Agent invocations: {metrics['agent_invocations']}")
print(f"Failures: {metrics['dead_letters']}")

# Per-stage metrics
for stage, duration in metrics["stage_durations"].items():
    print(f"{stage}: {duration}s")
```

## Workflow Integration

### GitHub Actions Integration

State persistence is integrated into workflows:

**Initialize project:**
```yaml
- name: Initialize State
  run: |
    python3 << 'PYTHON'
    import sys
    sys.path.insert(0, "somas")
    from core.state_manager import StateManager
    
    state_manager = StateManager()
    state_manager.initialize_project(
        project_id="${PROJECT_ID}",
        issue_number=${ISSUE_NUMBER},
        title="${TITLE}"
    )
    PYTHON
```

**Start stage:**
```yaml
- name: Start Stage
  run: |
    python3 << 'PYTHON'
    import sys
    sys.path.insert(0, "somas")
    from core.state_manager import StateManager
    
    state_manager = StateManager()
    state_manager.start_stage(
        project_id="${PROJECT_ID}",
        stage="implementation",
        agent="coder"
    )
    PYTHON
```

**Complete stage:**
```yaml
- name: Complete Stage
  run: |
    python3 << 'PYTHON'
    import sys
    sys.path.insert(0, "somas")
    from core.state_manager import StateManager
    
    state_manager = StateManager()
    state_manager.complete_stage(
        project_id="${PROJECT_ID}",
        stage="implementation",
        artifacts=["src/api.js"],
        create_checkpoint=True
    )
    PYTHON
```

## Migration Guide

### Migrating Existing Projects

For projects created before state persistence:

1. **Create state files manually:**
```bash
python3 << 'PYTHON'
from somas.core.state_manager import StateManager
import json

# Read existing metadata
with open('.somas/projects/project-123/metadata.json', 'r') as f:
    metadata = json.load(f)

# Initialize state from metadata
state_manager = StateManager()
state_manager.initialize_project(
    project_id=metadata['project_id'],
    issue_number=metadata['issue_number'],
    title=metadata.get('title', 'Migrated Project'),
    branch=metadata.get('branch', f"somas/{metadata['project_id']}")
)

print(f"Migrated {metadata['project_id']}")
PYTHON
```

2. **Update state to reflect current progress:**
```python
# Mark completed stages
for stage in ["ideation", "specification"]:
    state_manager.complete_stage(
        project_id="project-123",
        stage=stage,
        artifacts=[]
    )
```

### Backward Compatibility

The system maintains backward compatibility:

- Projects without state files continue to work
- State files are created on-demand
- Old `metadata.json` files are preserved
- Workflows gracefully handle missing state

## Best Practices

1. **Always create checkpoints**: Enable recovery by creating checkpoints at stage completion
2. **Record failures**: Always use `fail_stage()` to record failures in dead letters
3. **Include context**: Provide rich context when recording failures for better debugging
4. **Query smartly**: Use filters when querying transitions to avoid loading entire logs
5. **Monitor metrics**: Track dead letter counts and retry counts to detect systemic issues

## Troubleshooting

### State file not found

If state file is missing:
```python
# Check if state exists
state_path = Path(f".somas/projects/{project_id}/state.json")
if not state_path.exists():
    # Initialize state
    state_manager.initialize_project(project_id, ...)
```

### Corrupted state

If state is corrupted:
1. Check `transitions.jsonl` for last known good state
2. Restore from checkpoint if available
3. Manually reconstruct state from artifacts

### Recovery not working

If recovery fails:
1. Check `recovery_info.can_resume` in state
2. Verify checkpoint integrity
3. Check dead letters for unrecovered failures
4. Manually reset stage status if needed

## Schema Validation

JSON schemas are provided in `.somas/templates/`:

- `state_schema.json` - State file schema
- `dead_letters_schema.json` - Dead letters schema
- `transitions_schema.json` - Transition entry schema

Validate files using standard JSON Schema validators.

## See Also

- [SOMAS Documentation](./README.md)
- [Pipeline Architecture](./ARCHITECTURE.md)
- [Agent System](./AGENTS.md)
- [Troubleshooting Guide](./TROUBLESHOOTING.md)
