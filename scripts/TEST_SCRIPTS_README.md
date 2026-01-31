# SOMAS Workflow Test Scripts

This directory contains automated test scripts for validating SOMAS workflows based on the comprehensive [WORKFLOW_VALIDATION.md](../WORKFLOW_VALIDATION.md) guide.

## Overview

The test scripts automate the validation of the complete SOMAS pipeline from issue creation through PR generation, monitoring each stage and logging all steps.

## Test Scripts

### Individual Test Scripts

1. **test-workflow-simple-project.sh** - Tests the complete workflow with a simple project
   - Creates a somas-project issue
   - Monitors all 11 pipeline stages
   - Validates artifact generation
   - Verifies PR creation
   - Full end-to-end test (~15-30 minutes)

2. **test-workflow-bug-report.sh** - Tests bug report workflow
   - Creates a somas:bug issue
   - Validates triage and classification
   - Verifies appropriate workflow triggers
   - Quick test (~2-5 minutes)

3. **test-workflow-enhancement.sh** - Tests enhancement request workflow
   - Creates a somas:enhance issue
   - Validates feature request handling
   - Verifies appropriate routing
   - Quick test (~2-5 minutes)

### Master Test Script

- **test-workflow-all.sh** - Runs all test scenarios and generates combined report
  - Executes all individual tests sequentially
  - Generates combined log with all results
  - Provides final pass/fail summary

## Helper Library

- **lib/workflow-test-helpers.sh** - Common functions library
  - GitHub API interactions
  - Workflow monitoring and validation
  - Log management
  - Error handling
  - Reusable across all test scripts

## Prerequisites

### Required Tools

```bash
# GitHub CLI (gh)
gh --version  # Should be v2.0.0 or higher

# jq (JSON processor)
jq --version

# git
git --version
```

### Installation

**macOS:**
```bash
brew install gh jq
```

**Ubuntu/Debian:**
```bash
sudo apt-get install gh jq
```

**Windows (via Chocolatey):**
```bash
choco install gh jq
```

### Authentication

Authenticate with GitHub CLI:

```bash
gh auth login
```

Follow the prompts to authenticate. The scripts require:
- repo (full control)
- workflow (manage workflows)
- write:org (if testing in an organization)

## Usage

### Running Individual Tests

```bash
# Navigate to scripts directory
cd scripts

# Run simple project test
./test-workflow-simple-project.sh

# Run bug report test
./test-workflow-bug-report.sh

# Run enhancement test
./test-workflow-enhancement.sh
```

### Running All Tests

```bash
# Run all tests
./test-workflow-all.sh
```

### Custom Log File

```bash
# Specify custom log file location
LOG_FILE=/path/to/custom.log ./test-workflow-simple-project.sh
```

## Output

### Log Files

Each test generates a detailed log file:

- **log.txt** - Default log file for individual tests
- **log-test-workflow-*.txt** - Individual test logs when running all tests
- **workflow-tests-combined.log** - Combined log from all tests
- **workflow-logs/run-*.log** - Downloaded GitHub Actions logs

### Log File Contents

Logs include:
- Timestamp for each step
- GitHub API interactions (issue creation, PR creation)
- Workflow trigger events
- Workflow execution status
- Label changes
- Comment verification
- Artifact verification
- Error messages and warnings
- Final summary with pass/fail status

### Example Log Output

```
2026-01-31 09:00:00 | [INFO] SOMAS Workflow Test: Simple Project
2026-01-31 09:00:00 | [INFO] Log file initialized: log.txt
2026-01-31 09:00:05 | [SUCCESS] All required commands available
2026-01-31 09:00:06 | [SUCCESS] GitHub CLI authenticated
2026-01-31 09:00:10 | [SUCCESS] Issue #123 created successfully
2026-01-31 09:00:15 | [INFO] Waiting for workflow 'intake-triage.yml'...
2026-01-31 09:00:25 | [SUCCESS] Workflow triggered (run ID: 789)
```

## What Gets Tested

Based on [WORKFLOW_VALIDATION.md](../WORKFLOW_VALIDATION.md), the scripts validate:

### Phase 1: Issue Creation
- Issue template usage
- Auto-labeling
- Required fields validation

### Phase 2: Intake/Triage
- Workflow trigger (intake-triage.yml)
- Triage agent invocation
- Label application (somas:triaged, somas:dev)
- Triage comment posting

### Phase 3: Pipeline Execution
- Main pipeline trigger (somas-pipeline.yml)
- Stage progression (11 stages)
- Milestone creation and assignment
- Project board setup

### Phase 4: Artifact Generation
- Project structure creation
- Artifact files:
  - project_request.md
  - initial_plan.yml
  - SPEC.md
  - execution_plan.yml
  - ARCHITECTURE.md
  - Source code
  - Test suite
  - Documentation

### Phase 5: PR Creation
- Branch creation (somas/project-{issue_number})
- PR generation
- PR labels
- Quality gate checks

### Phase 6: Comments and Updates
- Agent comments on issue
- Status updates
- Pipeline completion notification

## Validation Checklist

Each test verifies:

- ✅ Issue created successfully
- ✅ Correct labels applied
- ✅ Workflows triggered
- ✅ Workflows completed successfully
- ✅ Project structure created
- ✅ Artifacts generated
- ✅ State files valid JSON
- ✅ PR created
- ✅ PR linked to issue
- ✅ Comments posted

## Cleanup

By default, test scripts **DO NOT** automatically clean up:
- Issues remain open for manual review
- PRs remain open for manual review
- Project files remain in .somas/projects/

This allows manual inspection of test results.

To enable automatic cleanup, modify the script variables:

```bash
CLEANUP_ON_SUCCESS=true
CLEANUP_ON_FAILURE=true
```

Or manually close resources:

```bash
# Close issue
gh issue close 123 --comment "Test completed"

# Close PR
gh pr close 456 --comment "Test completed"
```

## Troubleshooting

### Issue: Workflows Not Triggering

**Cause:** Labels may not match workflow triggers

**Solution:** Verify label names match workflow triggers:
```bash
cat .github/workflows/intake-triage.yml | grep "label.name"
```

### Issue: PR Not Created

**Cause:** Branch may not exist or SOMAS_PAT not configured

**Solution:** Check workflow logs:
```bash
gh run view <run-id> --log
```

### Issue: Authentication Failures

**Solution:** Re-authenticate GitHub CLI:
```bash
gh auth logout
gh auth login
```

### Issue: Timeout Errors

**Cause:** Workflow taking longer than expected

**Solution:** Increase timeout values in test scripts:
```bash
# In test script, modify wait times:
wait_for_workflow_trigger "workflow.yml" "${issue_number}" 120  # Increase from 60 to 120
```

## Integration with CI/CD

These scripts can be integrated into CI/CD pipelines:

```yaml
# .github/workflows/test-workflows.yml
name: Test SOMAS Workflows

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
  workflow_dispatch:

jobs:
  test-workflows:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup GitHub CLI
        run: |
          gh auth status || gh auth login --with-token <<< "${{ secrets.GITHUB_TOKEN }}"
      
      - name: Run Workflow Tests
        run: |
          cd scripts
          ./test-workflow-all.sh
      
      - name: Upload Logs
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: workflow-test-logs
          path: |
            log*.txt
            workflow-logs/
```

## Contributing

When adding new test scripts:

1. Use the helper library functions from `lib/workflow-test-helpers.sh`
2. Follow naming convention: `test-workflow-{scenario}.sh`
3. Add script to `TEST_SCRIPTS` array in `test-workflow-all.sh`
4. Update this README with new test description
5. Ensure script is executable: `chmod +x test-workflow-{scenario}.sh`

## Related Documentation

- [WORKFLOW_VALIDATION.md](../WORKFLOW_VALIDATION.md) - Comprehensive validation guide
- [.github/workflows/](../.github/workflows/) - Workflow definitions
- [.somas/config.yml](../.somas/config.yml) - SOMAS configuration

## Support

For issues with test scripts:
1. Check workflow logs: `gh run view <run-id> --log`
2. Review test log files
3. Verify GitHub CLI authentication
4. Check repository permissions
5. Open an issue with test logs attached
