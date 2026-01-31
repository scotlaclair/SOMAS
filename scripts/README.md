# SOMAS Scripts

## Overview

The scripts directory contains utility scripts for maintaining and managing the SOMAS repository. These scripts automate common maintenance tasks, package structure fixes, and repository configuration.

## Available Scripts

### Workflow Testing Scripts

See [TEST_SCRIPTS_README.md](TEST_SCRIPTS_README.md) for comprehensive documentation on workflow test automation.

**Quick overview:**
- `test-workflow-simple-project.sh` - Full end-to-end project workflow test
- `test-workflow-bug-report.sh` - Bug report workflow test
- `test-workflow-enhancement.sh` - Enhancement workflow test  
- `test-workflow-all.sh` - Master script running all test scenarios
- `lib/workflow-test-helpers.sh` - Reusable helper functions

**Usage:**
```bash
# Run all workflow tests
./scripts/test-workflow-all.sh

# Or run individual test
./scripts/test-workflow-simple-project.sh
```

### Maintenance Scripts

### `validate-consistency.sh`
**Purpose:** Validates cross-references and consistency across the entire repository

**What it does:**
- Checks that all agent configurations referenced in workflows exist
- Validates that skills referenced in `skill-rules.json` exist
- Ensures templates referenced by agents are present
- Validates YAML/JSON syntax in configuration files
- Checks documentation cross-references
- Verifies workflow dependencies

**Usage:**
```bash
# Make executable (first time only)
chmod +x scripts/validate-consistency.sh

# Run validation
./scripts/validate-consistency.sh
```

**Exit codes:**
- `0` - All validations passed
- `1` - Validation errors found (see output for details)

**Common issues it catches:**
- Missing agent configuration files
- Broken skill references
- Invalid YAML/JSON syntax
- Missing template files
- Broken documentation links

### `fix_python_structure.sh`
**Purpose:** Fixes Python package structure issues by removing misplaced subdirectories

**What it does:**
- Removes incorrect nested directories in `somas/agents/` that duplicate top-level packages
- Verifies the correct package structure exists
- Ensures clean Python package organization

**Usage:**
```bash
./scripts/fix_python_structure.sh
```

**Common issues it fixes:**
- `somas/agents/apo/` (should be `somas/apo/`)
- `somas/agents/core/` (should be `somas/core/`)
- `somas/agents/analytics/` (should be `somas/analytics/`)

### `setup-labels.sh`
**Purpose:** Creates and manages GitHub repository labels using the GitHub CLI

**What it does:**
- Reads label definitions from `.github/labels.yml`
- Creates all standard SOMAS labels in the repository
- Handles duplicate labels with optional force mode
- Provides colored output for operation status

**Prerequisites:**
- GitHub CLI (`gh`) installed and authenticated
- Repository write permissions
- `.github/labels.yml` file exists

**Usage:**
```bash
# Create labels (skip if they already exist)
./scripts/setup-labels.sh

# Force recreate labels (delete existing first)
./scripts/setup-labels.sh --force
```

**Label categories created:**
- **Priority:** `somas:priority-*` (critical, high, medium, low)
- **Type:** `somas:bug`, `somas:enhancement`, `somas:question`, etc.
- **Status:** `somas:status-*` (in-progress, blocked, review-needed)
- **Stage:** `somas:stage-*` (intake, planning, implementation, etc.)

## Script Requirements

### System Dependencies
- **bash:** All scripts require bash shell
- **git:** Version control operations
- **GitHub CLI:** For `setup-labels.sh` (install from https://cli.github.com/)

### File Permissions
Scripts should be executable:
```bash
chmod +x scripts/*.sh
```

## Usage Guidelines

### For Maintainers
- Run `fix_python_structure.sh` after major refactoring
- Use `setup-labels.sh` when initializing new repositories
- Test scripts in development branches before running on main

### For Contributors
- Scripts are typically run by maintainers during repository setup
- Check script output for any errors or warnings
- Report issues with scripts as bugs

### Automation
- Scripts can be integrated into GitHub Actions workflows
- Consider running `fix_python_structure.sh` in CI pipelines
- Use `setup-labels.sh` in repository initialization workflows

## Error Handling

### Common Issues
- **Permission denied:** Make scripts executable with `chmod +x`
- **GitHub CLI not authenticated:** Run `gh auth login`
- **Missing dependencies:** Install required tools (git, gh)

### Troubleshooting
- Check script output for specific error messages
- Verify file paths and permissions
- Ensure you're in the repository root directory

## Integration Points

- **`.github/labels.yml`:** Source of truth for label definitions
- **`.github/workflows/`:** Can call scripts for automated maintenance
- **`somas/` package:** Scripts maintain the Python package structure
- **GitHub Repository:** Scripts configure repository settings and labels

---

*Last updated: January 30, 2026 12:00 UTC*</content>
<parameter name="filePath">/Users/architect/Developer/projects/somas/scripts/README.md