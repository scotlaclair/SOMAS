# SOMAS Core Runner

The SOMAS Core Runner (`somas/core/runner.py`) is a command-line tool that executes AI agent tasks within the SOMAS pipeline.

## Purpose

The runner provides a secure, consistent interface for:
- Executing individual implementation tasks
- Managing agent configurations
- Loading context files
- Producing structured outputs
- Validating inputs for security

## Usage

### Basic Syntax

```bash
python3 somas/core/runner.py \
  --agent <agent_name> \
  --task_name <name> \
  --task_desc <description> \
  --context_files <file1,file2> \
  --output_path <path> \
  [--project_id <project-123>] \
  [--config <config_path>]
```

### Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--agent` | Yes | Name of the agent to use | `coder`, `architect`, `tester` |
| `--task_name` | Yes | Short name for the task | `"API Implementation"` |
| `--task_desc` | Yes | Detailed task description | `"Implement REST API endpoints"` |
| `--context_files` | Yes | Comma-separated file paths | `"SPEC.md,ARCHITECTURE.md"` |
| `--output_path` | Yes | Where to write output | `"artifacts/result.md"` |
| `--project_id` | No | Project identifier | `"project-123"` |
| `--config` | No | Config file path | `".somas/config.yml"` |

### Examples

#### Execute a code generation task

```bash
python3 somas/core/runner.py \
  --agent coder \
  --task_name "Core API Implementation" \
  --task_desc "Implement REST API endpoints for user management" \
  --context_files ".somas/projects/project-123/artifacts/SPEC.md,.somas/projects/project-123/artifacts/ARCHITECTURE.md" \
  --output_path ".somas/projects/project-123/artifacts/tasks/TASK-005_result.md" \
  --project_id "project-123"
```

#### Execute a testing task

```bash
python3 somas/core/runner.py \
  --agent tester \
  --task_name "Integration Testing" \
  --task_desc "Create integration tests for API endpoints" \
  --context_files ".somas/projects/project-123/artifacts/api_specs.yml" \
  --output_path ".somas/projects/project-123/artifacts/tasks/TASK-008_result.md" \
  --project_id "project-123"
```

## Security Features

### Path Validation

All file paths are validated to prevent path traversal attacks:

```python
# Valid
".somas/projects/project-123/artifacts/SPEC.md"

# Invalid (rejected)
"../../etc/passwd"
"/etc/passwd"
".somas/projects/../../../secrets"
```

### Project ID Validation

Project IDs must match the pattern `project-<number>`:

```python
# Valid
"project-123"
"project-456"

# Invalid (rejected)
"project-test"
"../project-123"
"project-123; rm -rf /"
```

### No Shell Injection

- All operations use Python APIs, not shell commands
- No `eval()` or `exec()` of user input
- Subprocess calls (if any) use list-based arguments

## Integration with Pipeline

The runner is invoked by the `stage-5-implementation` job in the SOMAS pipeline:

```yaml
- name: Execute Implementation Task
  env:
    TASK_ID: ${{ matrix.task_id }}
    TASK_NAME: ${{ matrix.task_name }}
    TASK_DESC: ${{ matrix.task_desc }}
    PROJECT_ID: ${{ needs.initialize-pipeline.outputs.project_id }}
  run: |
    python3 somas/core/runner.py \
      --agent "coder" \
      --task_name "${TASK_NAME}" \
      --task_desc "${TASK_DESC}" \
      --context_files "${CONTEXT_FILES}" \
      --output_path "${OUTPUT_PATH}" \
      --project_id "${PROJECT_ID}"
```

## Agent Configuration

The runner reads agent configurations from `.somas/config.yml`:

```yaml
agents:
  agent_configs:
    coder:
      provider: "gpt_5_2_codex"
      config_file: ".somas/agents/coder.yml"
      description: "Code generation with SOTA coding agent"
    
    architect:
      provider: "claude_opus_4_5"
      config_file: ".somas/agents/architect.yml"
      description: "System design with deepest reasoning"
```

When you specify `--agent coder`, the runner will:
1. Look up the `coder` configuration
2. Use the `gpt_5_2_codex` provider
3. Apply settings from `.somas/agents/coder.yml`

## Output Format

The runner produces structured Markdown output:

```markdown
# Task: Core API Implementation

**Description:** Implement REST API endpoints for user management

**Agent:** coder
**Provider:** gpt_5_2_codex

## Status

Task execution placeholder. Integration with actual AI agents pending.

## Metadata

\```json
{
  "task_name": "Core API Implementation",
  "task_description": "Implement REST API endpoints for user management",
  "agent": "coder",
  "provider": "gpt_5_2_codex",
  "context_files": [
    ".somas/projects/project-123/artifacts/SPEC.md",
    ".somas/projects/project-123/artifacts/ARCHITECTURE.md"
  ],
  "output_path": ".somas/projects/project-123/artifacts/tasks/TASK-005_result.md",
  "project_id": "project-123"
}
\```
```

## Error Handling

### Invalid Project ID

```
Error: Invalid project_id format: project-test
Exit code: 1
```

### Invalid Path

```
Error: Invalid output path: ../../etc/passwd
Exit code: 1
```

### Missing Context File

```
Warning: Could not read SPEC.md: [Errno 2] No such file or directory
Executing task: Core API Implementation
Agent: coder (Provider: gpt_5_2_codex)
Context files: 1
Task completed successfully. Output written to: ...
Exit code: 0
```

Note: Missing context files generate warnings but don't fail the task.

### Agent Not Found

```
Warning: Agent 'unknown' not found in config. Using defaults.
Executing task: ...
Exit code: 0
```

## Future Enhancements

The runner is designed for extensibility:

1. **Actual AI Agent Integration**: Replace placeholder with real LLM API calls
2. **Streaming Output**: Add support for streaming responses
3. **Caching**: Cache context files to reduce I/O
4. **Retry Logic**: Implement exponential backoff for transient failures
5. **Progress Tracking**: Add progress callbacks for long-running tasks
6. **Multi-Agent Coordination**: Support agent collaboration within a task

## Development

### Testing the Runner

```bash
# Create test project
mkdir -p .somas/projects/project-test/artifacts
echo "# Test Spec" > .somas/projects/project-test/artifacts/SPEC.md

# Run a test task
python3 somas/core/runner.py \
  --agent coder \
  --task_name "Test Task" \
  --task_desc "Testing the runner" \
  --context_files ".somas/projects/project-test/artifacts/SPEC.md" \
  --output_path ".somas/projects/project-test/artifacts/test_result.md" \
  --project_id "project-test"

# Check the output
cat .somas/projects/project-test/artifacts/test_result.md
```

### Adding Dependencies

The runner requires:
- Python 3.11+
- `pyyaml` for configuration parsing

Install with:
```bash
pip install pyyaml
```

## Troubleshooting

### ImportError: No module named 'yaml'

```bash
pip install pyyaml
```

### Invalid YAML in config

Check `.somas/config.yml` for syntax errors:
```bash
python3 -c "import yaml; yaml.safe_load(open('.somas/config.yml'))"
```

### Permission Denied

Ensure the runner is executable:
```bash
chmod +x somas/core/runner.py
```

## See Also

- [SOMAS Pipeline Documentation](../../docs/somas/README.md)
- [Agent Configuration Reference](../../.somas/agents/README.md)
- [Workflow Documentation](../../.github/workflows/README.md)
