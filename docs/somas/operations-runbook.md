# SOMAS Operations Runbook

This runbook provides operational procedures for managing the SOMAS autonomous pipeline.

## Table of Contents

- [Restarting Failed Pipelines](#restarting-failed-pipelines)
- [Circuit Breaker Management](#circuit-breaker-management)
- [Troubleshooting Procedures](#troubleshooting-procedures)
- [Monitoring](#monitoring)
- [Emergency Procedures](#emergency-procedures)

---

## Restarting Failed Pipelines

### Identifying Failed Pipelines

**Via GitHub Issues**:
1. Check issues with `somas:failed` label
2. Review issue comments for failure details
3. Check linked PR for error context

**Via State Files**:
```bash
# Find projects with failed status
grep -l '"status": "failed"' .somas/projects/*/state.json

# View specific project state
cat .somas/projects/<project-id>/state.json | jq '.status, .current_stage'
```

### Automatic Recovery

SOMAS attempts automatic recovery before escalating:

1. **Retry Logic**: Failed stages retry up to 3 times
2. **Debugger Agent**: Invoked automatically on validation failures
3. **Checkpoint Resume**: Pipeline resumes from last successful checkpoint

Check if automatic recovery is possible:
```bash
cat .somas/projects/<project-id>/state.json | jq '.recovery_info'
```

### Manual Restart Procedures

#### Restart from Specific Stage

1. Update project state to restart from desired stage:
   ```bash
   # View current state
   cat .somas/projects/<project-id>/state.json | jq '.'

   # Identify the stage to restart from
   # Edit state.json to set current_stage and status
   ```

2. Trigger pipeline via GitHub Actions:
   ```bash
   gh workflow run somas-pipeline.yml \
     -f project_id=<project-id> \
     -f start_stage=<stage-name>
   ```

#### Restart from Last Checkpoint

```bash
# Get last successful checkpoint
CHECKPOINT=$(cat .somas/projects/<project-id>/state.json | jq -r '.recovery_info.last_successful_checkpoint')

# Resume from checkpoint
gh workflow run somas-resume.yml \
  -f project_id=<project-id> \
  -f checkpoint_id=$CHECKPOINT
```

#### Full Pipeline Restart

Use when state is corrupted or partial restart won't work:

1. Archive current state:
   ```bash
   mv .somas/projects/<project-id> .somas/projects/<project-id>.backup.$(date +%Y%m%d)
   ```

2. Trigger fresh pipeline:
   ```bash
   gh workflow run somas-pipeline.yml -f issue_number=<issue-number>
   ```

### Post-Restart Verification

1. Monitor issue comments for stage progress
2. Check state file updates:
   ```bash
   watch -n 30 'cat .somas/projects/<project-id>/state.json | jq ".current_stage, .status"'
   ```
3. Verify no dead letters accumulated:
   ```bash
   cat .somas/projects/<project-id>/dead_letters.json | jq 'length'
   ```

---

## Circuit Breaker Management

### Understanding Circuit Breakers

Circuit breakers prevent cascading failures when external services fail:

| State | Description | Behavior |
|-------|-------------|----------|
| **Closed** | Normal operation | Requests proceed |
| **Open** | Service failing | Requests fail fast |
| **Half-Open** | Testing recovery | Limited requests |

### Checking Circuit Breaker Status

```bash
# View circuit breaker state (if tracked in state file)
cat .somas/projects/<project-id>/state.json | jq '.circuit_breakers'
```

### Manual Circuit Breaker Controls

#### Force Close (Reset)

When you've verified the service is healthy:

```python
from somas.core.circuit_breaker import CircuitBreaker

breaker = CircuitBreaker(service_name="ai_api")
breaker.reset()  # Force closed state
```

#### Force Open (Prevent Calls)

When you need to prevent API calls:

```python
breaker = CircuitBreaker(service_name="ai_api")
breaker.trip()  # Force open state
```

### Circuit Breaker Configuration

In `.somas/config.yml`:

```yaml
error_handling:
  circuit_breaker:
    failure_threshold: 5      # Failures before opening
    recovery_timeout: 60      # Seconds before half-open
    half_open_requests: 3     # Test requests in half-open
```

### Monitoring Circuit Breaker Events

Circuit breaker events are logged to transitions:
```bash
grep "circuit_breaker" .somas/projects/<project-id>/transitions.jsonl
```

---

## Troubleshooting Procedures

### Common Issues

#### 1. Pipeline Stuck at Stage

**Symptoms**: Stage shows `in_progress` for longer than timeout

**Diagnosis**:
```bash
# Check stage start time
cat .somas/projects/<project-id>/state.json | jq '.stages.<stage>.started_at'

# Check for recent transitions
tail -20 .somas/projects/<project-id>/transitions.jsonl
```

**Resolution**:
1. Check GitHub Actions for running workflows
2. Cancel stuck workflow if necessary
3. Reset stage status and restart

#### 2. Agent Not Responding

**Symptoms**: Issue comment requesting agent action, no response

**Diagnosis**:
```bash
# Check agent configuration
cat .somas/agents/<agent>.yml

# Verify workflow trigger
gh run list --workflow=somas-agent.yml
```

**Resolution**:
1. Verify agent configuration is valid YAML
2. Check API key is set in secrets
3. Manually trigger agent via issue comment

#### 3. State File Corruption

**Symptoms**: JSON parse errors, missing data

**Diagnosis**:
```bash
# Test JSON validity
python -c "import json; json.load(open('.somas/projects/<project-id>/state.json'))"
```

**Resolution**:
1. Restore from backup:
   ```bash
   cp .somas/projects/<project-id>/state.json.backup .somas/projects/<project-id>/state.json
   ```
2. Or reconstruct from transitions:
   ```bash
   # Review transitions for state reconstruction
   cat .somas/projects/<project-id>/transitions.jsonl | jq -s '.'
   ```

#### 4. Quality Gate Failures

**Symptoms**: Stage fails quality checks repeatedly

**Diagnosis**:
```bash
# View validation results
cat .somas/projects/<project-id>/artifacts/validation_report.json | jq '.'

# Check specific gate
cat .somas/projects/<project-id>/artifacts/test_results.json | jq '.failures'
```

**Resolution**:
1. Review failing gate criteria
2. Check if requirement is achievable
3. Adjust quality gate if overly strict
4. Manually address code issues

#### 5. Dead Letter Queue Growing

**Symptoms**: `dead_letters.json` accumulating entries

**Diagnosis**:
```bash
# Count dead letters
cat .somas/projects/<project-id>/dead_letters.json | jq 'length'

# View recent failures
cat .somas/projects/<project-id>/dead_letters.json | jq '.[-5:]'
```

**Resolution**:
1. Investigate root cause of failures
2. Process recoverable dead letters
3. Purge unrecoverable entries:
   ```bash
   # Backup then clear
   cp dead_letters.json dead_letters.json.backup
   echo "[]" > dead_letters.json
   ```

### Diagnostic Commands

```bash
# Full project health check
echo "=== Project Status ===" && \
cat .somas/projects/<project-id>/state.json | jq '.status, .current_stage' && \
echo "=== Recent Transitions ===" && \
tail -5 .somas/projects/<project-id>/transitions.jsonl && \
echo "=== Dead Letters ===" && \
cat .somas/projects/<project-id>/dead_letters.json | jq 'length'
```

---

## Monitoring

### Key Metrics to Watch

| Metric | Warning Threshold | Critical Threshold |
|--------|-------------------|-------------------|
| Pipeline duration | > 24 hours | > 72 hours |
| Stage retry count | > 2 | > 3 |
| Dead letter count | > 5 | > 10 |
| Human wait time | > 24 hours | > 48 hours |

### Transition Log Analysis

The `transitions.jsonl` file provides an audit trail:

```bash
# View all transitions for a project
cat .somas/projects/<project-id>/transitions.jsonl | jq -s '.'

# Filter by stage
cat .somas/projects/<project-id>/transitions.jsonl | jq 'select(.to_stage == "validation")'

# Find failures
grep '"status": "failed"' .somas/projects/<project-id>/transitions.jsonl
```

### Dead Letter Monitoring

```bash
# Watch for new dead letters
watch -n 60 'cat .somas/projects/<project-id>/dead_letters.json | jq "length"'

# Alert if threshold exceeded
if [ $(cat dead_letters.json | jq 'length') -gt 10 ]; then
  echo "ALERT: Dead letter threshold exceeded"
fi
```

### GitHub Actions Monitoring

```bash
# View recent workflow runs
gh run list --limit 20

# Check specific run
gh run view <run-id>

# Watch running workflow
gh run watch <run-id>
```

### Setting Up Alerts

Configure in `.somas/config.yml`:

```yaml
monitoring:
  alerts:
    enabled: true
    thresholds:
      pipeline_duration_hours: 168
      error_rate_percent: 20
      human_wait_time_hours: 48

  notifications:
    enabled: true
    notify_on:
      - "stage_completed"
      - "human_gate_opened"
      - "error_occurred"
      - "pipeline_completed"
```

---

## Emergency Procedures

### Stopping All Pipelines

When you need to halt all SOMAS activity:

1. **Cancel running workflows**:
   ```bash
   # List running workflows
   gh run list --status in_progress

   # Cancel all
   gh run list --status in_progress --json databaseId -q '.[].databaseId' | xargs -I {} gh run cancel {}
   ```

2. **Disable workflow triggers**:
   - Go to repo Settings > Actions > General
   - Select "Disable actions"

3. **Update config to prevent new runs**:
   ```yaml
   # .somas/config.yml
   pipeline:
     enabled: false  # Disable all stages
   ```

### Data Recovery

#### Recover from Backup

```bash
# List available backups
ls -la .somas/projects/<project-id>/*.backup

# Restore specific backup
cp .somas/projects/<project-id>/state.json.backup.20260101 \
   .somas/projects/<project-id>/state.json
```

#### Reconstruct State from Transitions

```bash
# Export transitions
cat .somas/projects/<project-id>/transitions.jsonl > transitions_backup.jsonl

# Analyze to determine correct state
cat transitions_backup.jsonl | jq -s 'group_by(.stage) | map({stage: .[0].stage, events: length})'
```

### Rollback Procedures

#### Rollback Code Changes

```bash
# Find last known good commit
git log --oneline .somas/projects/<project-id>/

# Rollback to specific commit
git checkout <commit-hash> -- .somas/projects/<project-id>/
```

#### Rollback Configuration

```bash
# Restore config from backup
git checkout HEAD~1 -- .somas/config.yml

# Or restore from specific commit
git checkout <commit-hash> -- .somas/config.yml
```

### Escalation Path

| Severity | Response Time | Actions |
|----------|---------------|---------|
| Low | 24 hours | Monitor, log ticket |
| Medium | 4 hours | Investigate, attempt auto-fix |
| High | 1 hour | Manual intervention, notify team |
| Critical | 15 minutes | Stop pipelines, notify owner |

**Escalation Contact**: @scotlaclair

### Post-Incident

1. Document incident in issue
2. Update transitions log with resolution
3. Review and update runbook if needed
4. Create follow-up issues for improvements

---

## Appendix: Quick Reference

### State File Locations

| File | Purpose |
|------|---------|
| `state.json` | Current pipeline state |
| `dead_letters.json` | Failed operations |
| `transitions.jsonl` | Audit log |

### Common Commands

```bash
# Project status
cat .somas/projects/<id>/state.json | jq '.status'

# Current stage
cat .somas/projects/<id>/state.json | jq '.current_stage'

# Recent activity
tail -10 .somas/projects/<id>/transitions.jsonl

# Failed projects
grep -l '"status": "failed"' .somas/projects/*/state.json
```

---

## See Also

- [Troubleshooting Guide](TROUBLESHOOTING.md) - Common issues
- [Configuration Reference](configuration-reference.md) - All settings
- [Developer Guide](developer-guide.md) - Technical details
