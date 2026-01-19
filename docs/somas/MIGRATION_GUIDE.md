# SOMAS Migration Guide

## Overview

This guide documents changes made to harden the SOMAS pipeline and address security, reliability, and maintainability concerns identified in the Copilot review of PR #2.

## Breaking Changes

### Configuration Consolidation

**Impact:** Medium - Requires configuration updates if custom values were used

#### Simulation Parameters
**Before:** Simulation parameters were defined in three locations:
- `.somas/config.yml` under `optimization.simulation`
- `.somas/agents/simulator.yml` under `simulation_parameters`
- `.somas/stages/simulation.yml` under `configuration`

**After:** All simulation parameters are now defined only in `.somas/config.yml` under `optimization.simulation`:
```yaml
optimization:
  simulation:
    enabled: true
    method: "monte_carlo"
    iterations: 1000
    confidence_interval: 0.90
```

**Migration:** Remove any custom simulation parameters from `simulator.yml` and `simulation.yml` and ensure they are defined in `config.yml`.

#### Project Board Columns
**Before:** Column definitions existed in both:
- `.github/project-template.yml`
- `.somas/config.yml` under `project_management.github_project.columns`

**After:** Columns are defined only in `.github/project-template.yml` to maintain single source of truth.

**Migration:** If you customized columns in `config.yml`, move those customizations to `project-template.yml`.

#### Risk Multipliers
**Before:** Risk multipliers were hardcoded in the simulator agent instructions:
```yaml
- External dependencies: 1.5x
- New technology: 2x
```

**After:** Risk multipliers are configurable in `.somas/config.yml`:
```yaml
optimization:
  risk_multipliers:
    external_dependencies: 1.5
    new_technology: 2.0
    high_complexity: 1.8
    integration_heavy: 1.7
```

**Migration:** Customize risk multipliers in `config.yml` to match your project needs.

## Security Improvements

### Input Validation
**What Changed:** Added validation for `project_id` parameter to prevent path traversal attacks.

**Impact:** Project IDs must now contain only alphanumeric characters, hyphens, and underscores.

**Migration:** Ensure your project ID generation follows this pattern: `^[a-zA-Z0-9_-]+$`

### Shell Injection Prevention
**What Changed:** Issue titles and other user input are now safely encoded using Python's JSON module instead of shell string interpolation.

**Impact:** None for normal usage. Malicious input is now properly sanitized.

## Robustness Improvements

### Error Handling
**What Changed:**
- Git operations now check for actual changes before committing
- Template file operations verify file existence before copying
- Proper error messages for missing dependencies

**Impact:** Workflows are more resilient to edge cases and provide better error messages.

### Division by Zero Protection
**What Changed:** Estimation accuracy calculations now handle zero estimates:
```yaml
# Before: (actual - estimated) / estimated * 100
# After:  estimated > 0 ? (actual - estimated) / estimated * 100 : null
```

**Impact:** Analytics won't crash on tasks with zero-hour estimates.

## Configuration Flexibility

### Ambiguity Detection
**What Changed:** "should" and "could" moved from `reject_patterns` to `flag_patterns` in specifier agent.

**Impact:** Specifications using "should" or "could" will be flagged for review but not automatically rejected.

**Rationale:** These words are often appropriate for non-functional requirements (e.g., "The system should respond within 2 seconds").

### Approvers Configuration
**What Changed:** Added documentation about using GitHub teams for approvers.

**Current:**
```yaml
approvers:
  - "@scotlaclair"
```

**Recommended:**
```yaml
approvers:
  - "@org-name/approvers-team"
```

**Migration:** Create a GitHub team for approvers and reference it in configuration for easier team management.

## GitHub Projects V2 Migration (Recommended)

### Current State
The SOMAS pipeline currently uses GitHub Projects Classic API, which is in maintenance mode.

### Why Migrate?
- **Long-term Support:** GitHub Projects V2 is the actively developed platform
- **Advanced Features:** Custom fields, better automation, improved performance
- **GraphQL API:** More flexible and powerful than the REST API

### Migration Path

1. **Update `.github/workflows/somas-project-sync.yml`:**
   Replace the REST API calls with GraphQL mutations. See the review comments on PR #2 for example code.

2. **Update Custom Fields:**
   The current `project-template.yml` defines custom fields that aren't supported by the Classic API. These will work properly once migrated to Projects V2.

3. **Update Documentation:**
   Update team documentation to reference the new Projects V2 interface.

### Timeline
This migration is optional but recommended. The Classic API continues to work, but new features are only being added to Projects V2.

## Testing Your Changes

### Validate Configuration Files
```bash
python3 << 'SCRIPT'
import yaml
files = [
    '.somas/config.yml',
    '.somas/agents/simulator.yml',
    '.github/workflows/somas-pipeline.yml'
]
for f in files:
    with open(f) as file:
        yaml.safe_load(file)
    print(f'✓ {f}')
SCRIPT
```

### Test Workflow Syntax
```bash
# If you have act installed (GitHub Actions local runner)
act -l

# Or validate on GitHub by creating a draft PR
```

### Verify Project ID Validation
```bash
# Valid project IDs
project-123
my_project
test-project-1

# Invalid (will be rejected)
../../../etc
project/../secrets
project with spaces
```

## Rollback Plan

If you encounter issues with the changes:

1. **Configuration Issues:** Previous configuration files are preserved in git history. You can extract values from commit `06d7baf` (before these changes).

2. **Workflow Issues:** If workflows fail, you can temporarily disable the new stages in `.somas/config.yml`:
```yaml
pipeline:
  stages:
    - id: "simulation"
      enabled: false  # Temporarily disable
```

3. **Complete Rollback:** Revert to the previous version:
```bash
git revert <commit-hash>
```

## Getting Help

If you encounter issues during migration:

1. Check the [Troubleshooting Guide](./TROUBLESHOOTING.md) (if available)
2. Review the [PR #2 review comments](https://github.com/scotlaclair/SOMAS/pull/2) for context
3. Open an issue with:
   - What you're trying to do
   - The error message or unexpected behavior
   - Your configuration (sanitized of secrets)

## Summary of Changes

### High Priority (Security & Bug Fixes)
- ✅ Division by zero protection in estimation calculations
- ✅ Path traversal attack prevention in project_id validation
- ✅ Shell injection prevention with proper JSON encoding
- ✅ js-yaml dependency installation for workflow execution
- ✅ Improved git operation error handling

### Configuration Improvements
- ✅ Single source of truth for simulation parameters
- ✅ Single source of truth for project board columns
- ✅ Configurable risk multipliers
- ✅ More flexible ambiguity detection

### Documentation
- ✅ GitHub Projects V2 migration recommendation
- ✅ Updated dates and placeholders
- ✅ Better inline documentation

---

*Last Updated: 2026-01-18*
