# Dynamic Parallel Orchestration

This document explains how SOMAS dynamically distributes implementation tasks across parallel GitHub Actions jobs based on Monte Carlo simulation results.

## Overview

### The Problem

Previously, the SOMAS pipeline had a disconnect between design and implementation:

- **Design (Stage 3 - Simulation)**: Generated `execution_plan.yml` with optimized parallel task phases
- **Reality (Stage 5 - Implementation)**: Ran as a single linear job, ignoring the simulation intelligence

### The Solution

The refactored pipeline now:

1. **Parses** the simulation's `execution_plan.yml`
2. **Extracts** parallel tasks from the optimal execution plan
3. **Dispatches** multiple GitHub Actions jobs that run in parallel
4. **Executes** each task independently using the `somas/core/runner.py` CLI

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ Stage 3: Simulation                                             │
│ - Runs Monte Carlo simulation (1000 iterations)                 │
│ - Generates execution_plan.yml with optimal task sequence       │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 4: Architecture                                           │
│ - Designs system components                                     │
│ - Creates ARCHITECTURE.md, API specs, data models               │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 4-B: Dispatch (NEW)                                       │
│ - Reads execution_plan.yml                                      │
│ - Extracts parallel tasks from first suitable phase            │
│ - Converts to GitHub Actions matrix format                     │
│ - Outputs JSON matrix                                           │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 5: Implementation (REFACTORED)                            │
│ - Uses matrix strategy from Stage 4-B                          │
│ - Spawns N parallel jobs (one per task)                        │
│ - Each job runs somas/core/runner.py independently             │
│ - All jobs commit results back to the repository               │
└─────────────────────────────────────────────────────────────────┘
```

## Workflow Changes

### New Job: `stage-4-b-dispatch`

**Purpose**: Parse simulation output and create a dynamic task matrix

**Inputs**:
- `execution_plan.yml` from Stage 3 (simulation)

**Outputs**:
- `matrix`: JSON object with task array
- `has_tasks`: Boolean indicating if tasks exist

**Process**:

1. **Validate** execution plan exists
2. **Check** YAML syntax validity
3. **Search** for first phase with `parallel_tasks`
4. **Extract** task metadata (task_id, name, description, duration)
5. **Convert** to JSON matrix format
6. **Fallback** to sequential mode if anything fails

**Example Output**:

```json
{
  "include": [
    {
      "task_id": "TASK-005",
      "task_name": "Core API Implementation",
      "task_desc": "Implement REST API endpoints",
      "duration": 12.3
    },
    {
      "task_id": "TASK-006",
      "task_name": "Frontend Component Library",
      "task_desc": "Create reusable UI components",
      "duration": 10.5
    }
  ]
}
```

### Refactored Job: `stage-5-implementation`

**Changes**:

1. **Added `strategy.matrix`**: Uses output from `stage-4-b-dispatch`
2. **Changed dependency**: Now depends on `stage-4-b-dispatch` instead of `stage-4-architecture`
3. **Added `fail-fast: false`**: Jobs continue even if one fails
4. **Added Python setup**: Installs Python 3.11 and dependencies
5. **Replaced linear execution**: Each matrix job runs independently

**Matrix Expansion**:

If `stage-4-b-dispatch` outputs 4 tasks, GitHub Actions will spawn 4 parallel jobs:

```
stage-5-implementation (TASK-005, Core API Implementation)
stage-5-implementation (TASK-006, Frontend Component Library)
stage-5-implementation (TASK-007, Authentication Module)
stage-5-implementation (TASK-004, Database Migration Scripts)
```

Each job receives its own task parameters via the matrix.

## Execution Plan Format

### Structure

```yaml
optimal_execution_plan:
  phase_1:
    name: "Foundation"
    duration: "8-12 hours"
    parallel_tasks:
      - task_id: "TASK-001"
        name: "Database Schema Design"
        duration: 6.5
      - task_id: "TASK-002"
        name: "API Contract Definition"
        duration: 4.2
  
  phase_2:
    name: "Core Implementation"
    duration: "18-24 hours"
    parallel_tasks:
      - task_id: "TASK-005"
        name: "Core API Implementation"
        duration: 12.3
        risk: "HIGH"
      - task_id: "TASK-006"
        name: "Frontend Component Library"
        duration: 10.5

simulation_results:
  mean_hours: 42.5
  p90_hours: 58.3

critical_path:
  - task_id: "TASK-005"
    probability: 0.95
```

### Required Fields

For each task in `parallel_tasks`:

- `task_id`: Unique identifier (e.g., "TASK-005")
- `name`: Human-readable task name
- `duration`: Estimated hours (float)
- `risk`: Optional risk level ("HIGH", "MEDIUM", "LOW")

### Phase Selection Logic

The dispatch job searches phases in order:
1. `phase_1`
2. `phase_2` (typically implementation phase)
3. `phase_3`
4. `phase_4`
5. `phase_5`

It selects the **first phase with non-empty `parallel_tasks`**.

## Fallback Behavior

### When Does Fallback Trigger?

1. **Missing file**: `execution_plan.yml` doesn't exist
2. **Invalid YAML**: Syntax errors in the file
3. **Empty phases**: No phases have `parallel_tasks`
4. **Parsing errors**: Python JSON conversion fails

### Fallback Mode

If any error occurs, the dispatch job outputs a **single sequential task**:

```json
{
  "include": [
    {
      "task_id": "FALLBACK-001",
      "task_name": "Sequential Implementation",
      "task_desc": "Execute implementation in sequential mode",
      "duration": 24
    }
  ]
}
```

This ensures the pipeline **never fails** due to simulation issues. It gracefully degrades to the old behavior.

## Task Runner Integration

Each parallel job invokes `somas/core/runner.py`:

```bash
python3 somas/core/runner.py \
  --agent "coder" \
  --task_name "${TASK_NAME}" \
  --task_desc "${TASK_DESC}" \
  --context_files "${CONTEXT_FILES}" \
  --output_path "${OUTPUT_PATH}" \
  --project_id "${PROJECT_ID}"
```

### Context Files

Each task receives:
- `SPEC.md`: Requirements specification
- `ARCHITECTURE.md`: System architecture
- `execution_plan.yml`: Simulation results

### Output Location

Task results are written to:
```
.somas/projects/{project_id}/artifacts/tasks/{task_id}_result.md
```

Example:
```
.somas/projects/project-123/artifacts/tasks/TASK-005_result.md
```

## Benefits

### 1. True Parallel Execution

**Before**: Single job, ~40 hours sequential

**After**: 4 parallel jobs, ~12 hours (longest task)

**Time Saved**: 70% reduction in wall-clock time

### 2. Respects Simulation Intelligence

The Monte Carlo simulation identifies:
- Which tasks can run in parallel
- Optimal task groupings
- Critical path tasks
- Risk factors

The implementation stage now **acts on this intelligence**.

### 3. Better Resource Utilization

GitHub Actions runners:
- Execute tasks concurrently
- Maximize throughput
- Reduce idle time

### 4. Graceful Degradation

If simulation fails or produces invalid output:
- Pipeline continues with fallback
- Single sequential task runs
- No pipeline breakage

### 5. Visibility

GitHub Actions UI shows:
- Individual task progress
- Which tasks are running/complete
- Per-task logs
- Failure isolation

## Example Scenario

### Simulation Output

```yaml
optimal_execution_plan:
  phase_2:
    parallel_tasks:
      - task_id: "TASK-005"
        name: "Core API Implementation"
        duration: 12.3
      - task_id: "TASK-006"
        name: "Frontend Components"
        duration: 10.5
      - task_id: "TASK-007"
        name: "Authentication Module"
        duration: 8.7
```

### GitHub Actions Execution

```
✓ stage-4-b-dispatch (completed in 15s)
  └─ Generated matrix with 3 tasks

⟳ stage-5-implementation (TASK-005) - running
  └─ Core API Implementation (12.3h estimated)

⟳ stage-5-implementation (TASK-006) - running
  └─ Frontend Components (10.5h estimated)

⟳ stage-5-implementation (TASK-007) - running
  └─ Authentication Module (8.7h estimated)
```

All three run **simultaneously**, completing in ~12.3 hours (the longest task).

### Sequential Equivalent

Without parallelization:
```
12.3h + 10.5h + 8.7h = 31.5 hours total
```

With parallelization:
```
max(12.3h, 10.5h, 8.7h) = 12.3 hours total
```

**Speedup**: 2.56x faster

## Limitations

### Current Limitations

1. **Single Phase**: Only executes tasks from one phase
   - Future: Support multi-phase orchestration
   
2. **No Dependencies**: Doesn't respect intra-phase dependencies
   - Future: Parse `depends_on` fields

3. **Fixed Context**: All tasks get same context files
   - Future: Task-specific context from simulation

4. **Placeholder Runner**: Runner doesn't invoke real AI agents yet
   - Future: Integrate with actual LLM providers

### GitHub Actions Constraints

- **Concurrency Limit**: GitHub Free tier allows 20 concurrent jobs
- **Runner Limits**: Self-hosted runners may have capacity constraints
- **Timeout**: Each job has a 6-hour timeout by default

## Monitoring

### Check Task Status

View the Actions tab in GitHub:

```
Workflow Run #123
├─ stage-4-b-dispatch ✓
├─ stage-5-implementation (TASK-005) ✓
├─ stage-5-implementation (TASK-006) ⟳
├─ stage-5-implementation (TASK-007) ✗
└─ stage-5-implementation (TASK-004) ⟳
```

### View Task Logs

Click on any job to see:
- Task execution logs
- Runner output
- Error messages
- Commit information

### Check Task Results

Task outputs are committed to:
```
.somas/projects/project-123/artifacts/tasks/
├── TASK-005_result.md
├── TASK-006_result.md
├── TASK-007_result.md
└── TASK-004_result.md
```

## Troubleshooting

### No Tasks Dispatched

**Symptom**: `stage-5-implementation` is skipped

**Causes**:
- `has_tasks` output is `false`
- `stage-4-b-dispatch` failed

**Solution**:
1. Check `stage-4-b-dispatch` logs
2. Verify `execution_plan.yml` exists
3. Validate YAML syntax: `yq eval . execution_plan.yml`

### Fallback Mode Activated

**Symptom**: Only one "Sequential Implementation" task runs

**Causes**:
- Simulation didn't generate valid YAML
- No phases have `parallel_tasks`
- YAML parsing failed

**Solution**:
1. Check `stage-3-simulation` output
2. Validate `execution_plan.yml` structure
3. Ensure at least one phase has tasks

### Task Failures

**Symptom**: Some matrix jobs fail

**Behavior**: Other jobs continue (due to `fail-fast: false`)

**Solution**:
1. View failed job logs
2. Check task result artifacts
3. Re-run failed jobs individually

### Python Import Errors

**Symptom**: `ImportError: No module named 'yaml'`

**Solution**: The workflow installs `pyyaml` automatically:
```yaml
- name: Install Python Dependencies
  run: pip install pyyaml
```

If it still fails, check Python setup step.

## Future Enhancements

### Phase 2: Multi-Phase Orchestration

Support sequential execution of multiple phases:

```
Phase 1 (Foundation) → 3 parallel tasks
  ↓ (all complete)
Phase 2 (Implementation) → 4 parallel tasks
  ↓ (all complete)
Phase 3 (Integration) → 2 parallel tasks
```

### Phase 3: Dependency Management

Parse task dependencies from execution plan:

```yaml
- task_id: "TASK-008"
  name: "Integration Testing"
  depends_on: ["TASK-005", "TASK-006"]
```

Wait for dependencies before starting tasks.

### Phase 4: Smart Context Loading

Provide task-specific context files:

```yaml
- task_id: "TASK-005"
  context_requirements:
    - "SPEC.md#API-Requirements"
    - "ARCHITECTURE.md#Backend-Architecture"
    - "data_models.yml"
```

### Phase 5: Real-Time Progress

Stream task progress to GitHub Issues:

```
TASK-005: Core API Implementation
├─ [████████░░] 80% complete
├─ Generated 12 files
├─ 45 tests passing
└─ ETA: 2.5 hours remaining
```

## See Also

- [SOMAS Core Runner Documentation](../../somas/core/README.md)
- [Optimization Guide](optimization-guide.md)
- [Execution Plan Template](../../.somas/templates/execution_plan.yml)
- [Pipeline Configuration](../../.somas/config.yml)
