# SOMAS Troubleshooting Guide

## Common Issues and Solutions

### Workflow Failures

#### Issue: "Invalid project_id" error
**Symptom:**
```
Error: Invalid project_id: ../my-project. Must contain only alphanumeric characters, hyphens, and underscores.
```

**Cause:** Project ID contains invalid characters (path traversal attempt or special characters).

**Solution:**
Ensure project IDs match the pattern: `^[a-zA-Z0-9_-]+$`
- ✅ Valid: `project-123`, `my_project`, `test-01`
- ❌ Invalid: `project/../secrets`, `my project`, `test@123`

---

#### Issue: "js-yaml module not found"
**Symptom:**
```
Error: Cannot find module 'js-yaml'
```

**Cause:** The js-yaml package isn't installed before the workflow tries to use it.

**Solution:**
This should be fixed in the latest version. If you see this error:
1. Verify you're using the latest workflow version
2. Check that the "Setup Node.js for YAML parsing" and "Install js-yaml" steps are present
3. Ensure the steps run before "Create Task Issues"

---

#### Issue: Git push fails with "no changes to commit"
**Symptom:**
```
Error: nothing to commit, working tree clean
fatal: No configured push destination
```

**Cause:** Workflow tries to commit when no files have changed.

**Solution:**
This is now handled gracefully. The workflow will display "No changes to commit" and continue. If you see a failure, ensure you're using the latest version with proper change detection:
```bash
if git status --porcelain .somas/projects/ | grep . >/dev/null; then
  # Commit only if changes exist
fi
```

---

#### Issue: Template file not found
**Symptom:**
```
cp: cannot stat '.somas/templates/SPEC.md': No such file or directory
```

**Cause:** Template files don't exist in the repository.

**Solution:**
The latest workflows automatically generate fallback content if templates are missing. If you want to use custom templates:

1. Create the templates directory:
```bash
mkdir -p .somas/templates/
```

2. Add your templates:
   - `SPEC.md` - Specification document template
   - `execution_plan.yml` - Execution plan template
   - `ARCHITECTURE.md` - Architecture document template

---

### Configuration Issues

#### Issue: Division by zero in analytics
**Symptom:**
```
ZeroDivisionError: division by zero in estimation_error_percent calculation
```

**Cause:** Task has zero estimated duration.

**Solution:**
This is now handled. Estimation accuracy returns `null` instead of crashing:
```yaml
estimation_error_percent: null  # When estimated_duration_hours is 0
```

If you're processing analytics data, handle null values:
```python
if metric['estimation_error_percent'] is not None:
    # Process the metric
```

---

#### Issue: Duplicate configuration parameters
**Symptom:**
Confusion about which configuration values are being used.

**Cause:** Configuration parameters were defined in multiple files.

**Solution:**
After the hardening updates:
- **Simulation parameters:** Only in `.somas/config.yml` under `optimization.simulation`
- **Project columns:** Only in `.github/project-template.yml`
- **Risk multipliers:** Only in `.somas/config.yml` under `optimization.risk_multipliers`

Check the [Migration Guide](./MIGRATION_GUIDE.md) for details.

---

#### Issue: Specification rejected for using "should" or "could"
**Symptom:**
```
Quality gate failed: Ambiguous language detected
Pattern rejected: "should"
```

**Cause:** You're using an older version where "should" and "could" were in `reject_patterns`.

**Solution:**
These words are now in `flag_patterns` instead, meaning they'll be flagged for human review but not automatically rejected. Update to the latest `.somas/agents/specifier.yml`.

---

### Simulation & Optimization Issues

#### Issue: Simulation stage takes too long
**Symptom:**
Simulation stage runs for more than expected, consuming pipeline time.

**Cause:** High iteration count or complex task graphs.

**Solution:**
Adjust simulation parameters in `.somas/config.yml`:
```yaml
optimization:
  simulation:
    iterations: 500  # Reduce from 1000 for faster results
```

Trade-off: Fewer iterations = less accurate predictions. For most projects, 500-1000 iterations is appropriate.

---

#### Issue: High-risk tasks not being flagged
**Symptom:**
Tasks that should be high-risk aren't being identified.

**Cause:** Risk multipliers may not match your project's characteristics.

**Solution:**
Tune risk multipliers in `.somas/config.yml`:
```yaml
optimization:
  risk_multipliers:
    external_dependencies: 2.0  # Increase if external deps are risky
    new_technology: 2.5         # Increase for cutting-edge tech
    high_complexity: 2.0        # Increase for complex domains
    integration_heavy: 1.5      # Adjust based on integration pain
```

---

### GitHub Project Integration Issues

#### Issue: Project board not created
**Symptom:**
Pipeline runs but no GitHub Project board appears.

**Cause:** 
1. Insufficient permissions
2. Project sync workflow not triggered
3. Using GitHub Projects V2 (Classic API doesn't work)

**Solution:**
1. Verify permissions in workflow file:
```yaml
permissions:
  contents: write
  issues: write
  projects: write
```

2. Check workflow logs for dispatch events

3. If using Projects V2, see [Migration Guide](./MIGRATION_GUIDE.md) for GraphQL API migration

---

#### Issue: Task issues not created from execution plan
**Symptom:**
Simulation completes but no task issues are created.

**Cause:**
1. Execution plan file missing or malformed
2. js-yaml not installed
3. Project metadata missing

**Solution:**
1. Check that execution plan was created:
```bash
ls -la .somas/projects/project-*/artifacts/execution_plan.yml
```

2. Verify execution plan structure:
```yaml
optimal_execution_plan:
  phase_1:
    parallel_tasks:
      - task_id: "TASK-001"
        name: "Task name"
        duration: 4
```

3. Check workflow logs for specific errors

---

### Analytics & Metrics Issues

#### Issue: Privacy fields not anonymized
**Symptom:**
Developer names appear in analytics despite anonymization being enabled.

**Cause:** The fields listed in `privacy.fields_to_anonymize` are not currently collected in metric schemas.

**Solution:**
This is documented behavior. The privacy configuration is reserved for future implementation. If you need developer tracking with anonymization, you'll need to:
1. Add the fields to metric schemas
2. Implement collection logic
3. Implement anonymization logic

See `.somas/analytics/schema.yml` for notes.

---

#### Issue: Historical data not loading for simulations
**Symptom:**
Simulations don't use historical data for duration estimates.

**Cause:** Not enough historical data or data format mismatch.

**Solution:**
1. Check minimum samples required:
```yaml
models:
  duration_estimator:
    training_data_min_samples: 50  # Need at least this many samples
```

2. Verify data format in `.somas/analytics/runs/`:
```json
{"project_id": "...", "task_type": "...", "actual_duration_hours": 4.5}
```

3. Let the system accumulate more data over multiple runs

---

## Debugging Tips

### Enable Verbose Logging
In `.somas/config.yml`:
```yaml
development:
  verbose_logging: true
  save_intermediate_states: true
```

### Check Workflow Logs
1. Go to Actions tab in GitHub
2. Click on the failed workflow run
3. Expand failed steps to see detailed logs

### Validate Configuration Files
```bash
# Validate all YAML files
python3 << 'SCRIPT'
import yaml
import sys

files = [
    '.somas/config.yml',
    '.somas/agents/simulator.yml',
    '.somas/agents/specifier.yml',
    '.somas/stages/simulation.yml',
    '.github/workflows/somas-pipeline.yml'
]

for f in files:
    try:
        with open(f) as file:
            yaml.safe_load(file)
        print(f'✓ {f}')
    except Exception as e:
        print(f'✗ {f}: {e}')
        sys.exit(1)
SCRIPT
```

### Test Locally
Use [act](https://github.com/nektos/act) to test workflows locally:
```bash
# Install act
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run workflow
act -j stage-1-ideation
```

---

## Getting More Help

### Before Opening an Issue
1. Check this troubleshooting guide
2. Review [Migration Guide](./MIGRATION_GUIDE.md)
3. Check [PR #2 review comments](https://github.com/scotlaclair/SOMAS/pull/2)
4. Search existing issues for similar problems

### When Opening an Issue
Include:
- **What you're trying to do**
- **What happened instead**
- **Error messages** (full text, not screenshots)
- **Configuration** (sanitized of secrets)
- **Workflow run link** (if applicable)
- **Steps to reproduce**

### Emergency Rollback
If the pipeline is completely broken:
```bash
# Revert to last working commit
git revert HEAD

# Or disable problematic stages
# Edit .somas/config.yml:
pipeline:
  stages:
    - id: "simulation"
      enabled: false
```

---

## Performance Optimization

### Speed Up Pipeline Execution

1. **Reduce simulation iterations:**
```yaml
optimization:
  simulation:
    iterations: 500  # Down from 1000
```

2. **Increase parallelization:**
```yaml
optimization:
  parallelization:
    max_concurrent_tasks: 10  # Up from 5
```

3. **Disable optional features:**
```yaml
analytics:
  enabled: false  # Temporarily disable for speed

learning:
  enabled: false  # Disable ML model training
```

---

## Security Best Practices

### Protect Sensitive Data
- Never commit API keys to configuration files
- Use GitHub Secrets for credentials
- Review `.gitignore` to exclude sensitive files

### Validate External Input
The pipeline now validates:
- Project IDs (alphanumeric, hyphens, underscores only)
- Issue titles (properly escaped)
- File paths (no directory traversal)

### Keep Dependencies Updated
```bash
# Check for workflow updates
git fetch origin
git log origin/main..HEAD --oneline

# Review security advisories
# Visit: https://github.com/scotlaclair/SOMAS/security/advisories
```

---

*Last Updated: 2026-01-18*

For additional help, contact @scotlaclair or open an issue.
