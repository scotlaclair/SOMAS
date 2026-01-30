# SOMAS Configuration Reference

This document provides a complete reference for all SOMAS configuration options.

## Table of Contents

- [Main Configuration](#main-configuration)
- [Pipeline Stages](#pipeline-stages)
- [Agent Configuration](#agent-configuration)
- [APO Settings](#apo-settings)
- [State Manager Settings](#state-manager-settings)
- [Limits Configuration](#limits-configuration)
- [Quality Gates](#quality-gates)
- [Analytics Settings](#analytics-settings)

---

## Main Configuration

The main configuration file is located at `.somas/config.yml`.

### Top-Level Settings

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `version` | string | `"1.0.0"` | Configuration schema version |
| `name` | string | - | Project name |
| `description` | string | - | Project description |

### Example

```yaml
version: "1.0.0"
name: "Self-Sovereign Orchestrated Multi-Agent System"
description: "Configuration for AI-driven software development pipeline"
```

---

## Pipeline Stages

### Stage Configuration Table

| Stage | Order | Code Name | Agent | Human Gate | Timeout |
|-------|-------|-----------|-------|------------|---------|
| signal | 1 | SIGNAL | planner | No | 2h |
| design | 2 | DESIGN | specifier | No | 24h |
| grid | 3 | GRID | simulator | No | 2h |
| line | 4 | LINE | decomposer | No | 4h |
| mcp | 5 | MCP | coder | No | 48h |
| pulse | 6 | PULSE | validator | No | 12h |
| synapse | 7 | SYNAPSE | merger | No | 8h |
| overload | 8 | OVERLOAD | tester | No | 16h |
| velocity | 9 | VELOCITY | deployer | No | 24h |
| vibe | 10 | VIBE | operator | No | 8h |
| whole | 11 | WHOLE | analyzer | No | 4h |

### Stage Configuration Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique stage identifier |
| `order` | integer | Yes | Execution order (1-11) |
| `code_name` | string | Yes | Neurology-inspired stage name |
| `description` | string | Yes | Human-readable description |
| `enabled` | boolean | Yes | Whether stage is active |
| `agent` | string | Yes | Primary agent for this stage |
| `human_gate` | boolean | Yes | Requires human approval |
| `auto_proceed` | boolean | No | Automatically proceed to next stage |
| `timeout_hours` | integer | Yes | Maximum execution time |
| `max_retries` | integer | No | Retry count for failures (default: 3) |
| `feedback_loop_enabled` | boolean | No | Enable spec-simulation feedback |
| `max_feedback_iterations` | integer | No | Max feedback loop iterations |
| `execution_mode` | string | No | `single_shot` or `iterative` |

### Example Stage Configuration

```yaml
pipeline:
  stages:
    - id: "pulse"
      order: 6
      code_name: "PULSE"
      description: "Verify - Run tests, check heartbeat"
      enabled: true
      agent: "validator"
      human_gate: false
      auto_proceed: true
      timeout_hours: 12
      max_retries: 3
```

---

## Agent Configuration

### Provider Configuration

Providers define AI model settings:

| Field | Type | Description |
|-------|------|-------------|
| `model` | string | Model identifier (e.g., `claude-sonnet-4.5`) |
| `temperature` | float | Response randomness (0.0-1.0) |
| `max_tokens` | integer | Maximum response tokens |
| `description` | string | Provider description |

### Available Providers

| Provider | Model | Temperature | Max Tokens | Best For |
|----------|-------|-------------|------------|----------|
| `claude_opus_4_5` | claude-opus-4.5 | 0.7 | 8000 | Deep reasoning, architecture |
| `claude_sonnet_4_5` | claude-sonnet-4.5 | 0.5 | 8000 | Balanced coding tasks |
| `claude_haiku_4_5` | claude-haiku-4.5 | 0.4 | 4000 | Fast debugging |
| `gpt_5_2` | gpt-5.2 | 0.7 | 8000 | Requirements, security |
| `gpt_5_2_codex` | gpt-5.2-codex | 0.3 | 8000 | Code generation |
| `gemini_3_pro` | gemini-3-pro | 0.5 | 32000 | Documentation, long context |
| `grok_code_fast_1` | grok-code-fast-1 | 0.3 | 4000 | Low-latency orchestration |

### Agent Configuration Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `provider` | string | Yes | Primary AI provider |
| `fallback` | string | No | Fallback provider on failure |
| `config_file` | string | Yes | Path to agent YAML config |
| `description` | string | Yes | Agent description |

### Example Agent Configuration

```yaml
agents:
  providers:
    claude_sonnet_4_5:
      model: "claude-sonnet-4.5"
      temperature: 0.5
      max_tokens: 8000
      description: "Balanced power for testing and review"

  agent_configs:
    validator:
      provider: "claude_sonnet_4_5"
      fallback: "grok_code_fast_1"
      config_file: ".somas/agents/validator.yml"
      description: "Validation with balanced power"
```

---

## APO Settings

Autonomous Prompt Optimization enhances all agent prompts.

### Core APO Settings

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable APO for all agents |
| `version` | string | `"1.0.0"` | APO version |
| `auto_model_selection` | boolean | `true` | Auto-select mental models |
| `require_reasoning_trail` | boolean | `true` | Document reasoning process |
| `verification_required` | boolean | `true` | Require quality verification |
| `max_iterations` | integer | `3` | Max quality loop iterations |

### Mental Models Configuration

| Field | Type | Description |
|-------|------|-------------|
| `enabled_models` | list | Active mental models |
| `library_path` | string | Path to models definition |
| `agent_preferences` | object | Per-agent model preferences |

### Available Mental Models

| Model | Description | Best For |
|-------|-------------|----------|
| `first_principles` | Break down to fundamental truths | Architecture, design |
| `inversion` | Consider what could go wrong | Validation, security |
| `second_order_thinking` | Consider downstream effects | Specification |
| `ooda_loop` | Observe, Orient, Decide, Act | Implementation |
| `occams_razor` | Prefer simpler solutions | Code generation |
| `six_thinking_hats` | Multiple perspective analysis | Validation |
| `tree_of_thoughts` | Branching exploration | Simulation, planning |

### Task Analyzer Settings

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable task analysis |
| `minimum_complexity_for_apo` | float | `2.0` | APO threshold |
| `complexity_thresholds.simple` | float | `2.0` | Simple task max |
| `complexity_thresholds.moderate` | float | `3.5` | Moderate task max |
| `complexity_thresholds.complex` | float | `5.0` | Complex task max |

### Example APO Configuration

```yaml
apo:
  enabled: true
  auto_model_selection: true
  max_iterations: 3

  mental_models:
    enabled_models:
      - "first_principles"
      - "inversion"
      - "ooda_loop"

    agent_preferences:
      architect:
        prefer: ["first_principles", "occams_razor"]

  task_analyzer:
    minimum_complexity_for_apo: 2.0
    auto_routing:
      enabled: true
      rules:
        - complexity: "> 3.5"
          model: "claude_opus_4_5"
          chain: "draft_critique_refine"
```

---

## State Manager Settings

Controls state persistence and checkpoint management.

### Configuration Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `max_checkpoints` | integer | `20` | Checkpoints to retain |

### Checkpointing Settings

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | boolean | Enable checkpointing |
| `storage` | string | Storage backend (`github_artifacts`) |
| `frequency` | string | Checkpoint frequency (`per_stage`) |
| `save_state` | list | State elements to save |

### Recovery Settings

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `auto_resume` | boolean | `true` | Auto-resume on failure |
| `max_resume_attempts` | integer | `3` | Max resume attempts |
| `resume_strategy` | string | `from_last_checkpoint` | Resume strategy |

### Example Configuration

```yaml
state_manager:
  max_checkpoints: 20

checkpointing:
  enabled: true
  storage: "github_artifacts"
  frequency: "per_stage"

  save_state:
    - "project_metadata"
    - "stage_outputs"
    - "execution_context"

  recovery:
    auto_resume: true
    max_resume_attempts: 3
```

---

## Limits Configuration

### Iteration Limits

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `per_stage` | integer | `3` | Max iterations per stage |
| `per_feedback_loop` | integer | `2` | Max feedback iterations |
| `per_project` | integer | `8` | Max total project iterations |

### Workflow Limits

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `workflow_runtime_mins` | integer | `300` | GitHub Actions timeout |

### Example Configuration

```yaml
limits:
  api_calls: none  # Unlimited for subscription

  iterations:
    per_stage: 3
    per_feedback_loop: 2
    per_project: 8

  workflow_runtime_mins: 300
```

---

## Quality Gates

Quality gates define criteria that must pass before proceeding.

### Gates by Stage

#### Specification Gates

```yaml
quality_gates:
  specification:
    - "All requirements have unique IDs"
    - "All requirements are testable"
    - "No ambiguous language (TBD, maybe, etc.)"
    - "Open questions resolved or escalated"
    - "Security requirements defined"
```

#### Simulation Gates

```yaml
quality_gates:
  simulation:
    - "Task graph is acyclic"
    - "All tasks have duration estimates"
    - "Critical path identified"
    - "Parallelization opportunities documented"
```

#### Architecture Gates

```yaml
quality_gates:
  architecture:
    - "All components defined"
    - "Interfaces specified"
    - "Data flows documented"
    - "Technology choices justified"
```

#### Implementation Gates

```yaml
quality_gates:
  implementation:
    - "All tests passing"
    - "Code coverage > 80%"
    - "No critical security vulnerabilities"
    - "Documentation complete"
```

#### Validation Gates

```yaml
quality_gates:
  validation:
    - "All acceptance criteria met"
    - "Performance requirements satisfied"
    - "Security scan passed"
    - "Integration tests passing"
```

---

## Analytics Settings

### Core Analytics Configuration

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable analytics |
| `storage` | string | `.somas/analytics/runs/` | Storage path |
| `retention_days` | integer | `90` | Data retention |

### Tracked Metrics

```yaml
analytics:
  track:
    - "task_duration_vs_estimate"
    - "iteration_count_by_task_type"
    - "parallel_efficiency"
    - "critical_path_accuracy"
    - "human_intervention_frequency"
```

### Learning Configuration

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable learning |
| `record_all_runs` | boolean | `true` | Record all executions |
| `update_estimates_from_actuals` | boolean | `true` | Improve estimates |
| `pattern_extraction` | boolean | `true` | Extract patterns |

### Example Configuration

```yaml
analytics:
  enabled: true
  storage: ".somas/analytics/runs/"
  retention_days: 90

  track:
    - "task_duration_vs_estimate"
    - "parallel_efficiency"

learning:
  enabled: true
  update_estimates_from_actuals: true
```

---

## Environment Configuration

### Development Environment

```yaml
environments:
  dev:
    branch_pattern: "somas/*"
    auto_proceed: true
    human_gates: []
    auto_merge: true
```

### Production Environment

```yaml
environments:
  prod:
    branch_pattern: "main"
    human_gates: ["production_deployment"]
    require_approval_from: ["@scotlaclair"]
    auto_merge: false
```

---

## File Locations

| Configuration | Location |
|---------------|----------|
| Main config | `.somas/config.yml` |
| Agent configs | `.somas/agents/*.yml` |
| Stage configs | `.somas/stages/*.yml` |
| APO mental models | `.somas/apo/mental-models.yml` |
| APO task analyzer | `.somas/apo/task-analyzer.yml` |
| APO chains | `.somas/apo/chains/` |
| Analytics schema | `.somas/analytics/schema.yml` |

---

## See Also

- [Developer Guide](developer-guide.md) - Extending SOMAS
- [APO Guide](apo-guide.md) - Autonomous Prompt Optimization
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues
