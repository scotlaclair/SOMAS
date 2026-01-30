# SOMAS Cross-Reference Matrix

## Overview

This document maps all cross-references in the SOMAS repository to ensure consistency when making changes. Each section shows what files reference each other and how changes propagate.

## 1. Configuration References

### `.somas/config.yml` (Central Configuration)
**Referenced by:**
- `.github/workflows/somas-pipeline.yml` - Pipeline stages and agent assignments
- `.github/workflows/somas-orchestrator.yml` - Orchestrator behavior
- `.github/copilot-config.yml` - Copilot agent configurations
- `.somas/agents/*.yml` - Individual agent configurations reference limits and settings
- `docs/somas/configuration-reference.md` - Documentation

**References:**
- `.somas/agents/*.yml` - Agent configuration files
- `.somas/templates/*.md` - Template files
- `.somas/stages/*.yml` - Stage definitions

**Change Impact:** Changes here affect pipeline behavior, agent capabilities, and documentation

---

## 2. Agent Configuration References

### `.somas/agents/*.yml` (Individual Agent Configs)
**Referenced by:**
- `.somas/config.yml` - Agent assignments and config file paths
- `.github/workflows/somas-pipeline.yml` - Agent execution parameters
- `.github/copilot-config.yml` - Copilot agent mappings
- `docs/somas/agents/` - Agent documentation

**References:**
- `.somas/config.yml` - Global settings and limits
- `.somas/templates/*.md` - Output templates
- `skills/` - Skill implementations

**Change Impact:** Agent behavior changes affect pipeline execution and output quality

---

## 3. Skill System References

### `skill-rules.json` (Skill Activation Rules)
**Referenced by:**
- `.github/workflows/` - Skill-based workflow triggers
- `.somas/agents/` - Agent skill activation
- `scripts/` - Skill management scripts

**References:**
- `skills/*/` - Skill implementation directories
- `.somas/agents/` - Agent configurations

**Change Impact:** Skill rule changes affect when and how agents activate

### `skills/*/` (Skill Implementations)
**Referenced by:**
- `skill-rules.json` - Activation rules
- `.somas/agents/` - Agent skill usage
- `docs/skills/` - Skill documentation

**References:**
- None (leaf nodes)

**Change Impact:** Skill implementation changes affect agent capabilities

---

## 4. Template References

### `.somas/templates/*.md` (Output Templates)
**Referenced by:**
- `.somas/agents/*.yml` - Template specifications
- `.somas/config.yml` - Default templates
- `scripts/` - Template validation

**References:**
- None (static content)

**Change Impact:** Template changes affect all generated outputs

---

## 5. Documentation References

### `docs/somas/*.md` (Core Documentation)
**Referenced by:**
- `README.md` - Main project documentation
- `.somas/agents/` - Agent documentation links
- `CONTRIBUTING.md` - Development guides

**References:**
- `.somas/config.yml` - Configuration examples
- `.somas/agents/` - Agent details
- `skills/` - Skill documentation

**Change Impact:** Documentation changes affect contributor understanding

---

## 6. Workflow References

### `.github/workflows/*.yml` (GitHub Actions)
**Referenced by:**
- `.github/workflow-templates/` - Template definitions
- `docs/somas/operations-runbook.md` - Operational procedures

**References:**
- `.somas/config.yml` - Pipeline configuration
- `.somas/agents/` - Agent configurations
- `scripts/` - Utility scripts
- `requirements.txt` - Python dependencies

**Change Impact:** Workflow changes affect CI/CD pipeline behavior

---

## 7. Dependency References

### `requirements.txt` (Python Dependencies)
**Referenced by:**
- `.github/workflows/*.yml` - CI/CD environments
- `docs/somas/getting-started.md` - Setup instructions
- `scripts/` - Python-based utilities

**References:**
- None (external packages)

**Change Impact:** Dependency changes affect all Python execution environments

---

## 8. Script References

### `scripts/*.sh` (Utility Scripts)
**Referenced by:**
- `.github/workflows/*.yml` - CI/CD automation
- `docs/somas/operations-runbook.md` - Operational procedures
- `CONTRIBUTING.md` - Development workflows

**References:**
- `.somas/config.yml` - Configuration access
- `skill-rules.json` - Skill management
- Various directories - File operations

**Change Impact:** Script changes affect automation and maintenance procedures

---

## Consistency Validation

### Automated Checks
Run `scripts/validate-consistency.sh` to check:
- All referenced files exist
- Configuration files have valid syntax
- Cross-references are unbroken
- Dependencies are properly declared

### Manual Verification Checklist

#### When modifying `.somas/config.yml`:
- [ ] Update all referencing workflows
- [ ] Update agent configurations if limits changed
- [ ] Update documentation examples
- [ ] Run validation script

#### When adding/removing agents:
- [ ] Update `.somas/config.yml` agent assignments
- [ ] Update workflow agent references
- [ ] Update copilot configurations
- [ ] Add/remove agent documentation

#### When modifying skills:
- [ ] Update `skill-rules.json` if triggers changed
- [ ] Update agent configurations if skill usage changed
- [ ] Update skill documentation

#### When changing templates:
- [ ] Update all agents that reference the template
- [ ] Update template validation in scripts
- [ ] Update documentation examples

#### When updating dependencies:
- [ ] Update all workflow Python environments
- [ ] Update setup documentation
- [ ] Test all Python execution paths

---

## Change Propagation Rules

### 1. Configuration Changes
**Rule:** Changes to `.somas/config.yml` must be validated against all dependent systems
**Action:** Run full validation suite and update all references

### 2. Agent Changes
**Rule:** Agent configuration changes affect pipeline execution
**Action:** Test pipeline end-to-end and update documentation

### 3. Skill Changes
**Rule:** Skill changes affect agent behavior
**Action:** Update skill rules and test agent activation

### 4. Template Changes
**Rule:** Template changes affect all generated content
**Action:** Validate all template usage and update examples

### 5. Dependency Changes
**Rule:** Dependency changes affect all execution environments
**Action:** Update all CI/CD workflows and documentation

---

## Tools for Consistency

### Validation Scripts
- `scripts/validate-consistency.sh` - Comprehensive cross-reference validation
- `scripts/fix_python_structure.sh` - Python package structure fixes

### CI/CD Integration
- PR Security workflow validates dependencies
- CodeQL workflow checks code quality
- Automated validation on pushes to main

### Documentation
- This cross-reference matrix
- Individual README files in each directory
- Index files for machine-readable navigation

---

*Last updated: January 30, 2026*