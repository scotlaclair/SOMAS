# SOMAS Label System

This directory contains the configuration and setup scripts for SOMAS's comprehensive label system used for workflow triggers, triage, state machine orchestration, and automation.

## Overview

The SOMAS label system consists of several categories:

- **Core Pipeline Labels**: Trigger and identify SOMAS projects
- **Triage Labels**: Classify and route incoming requests
- **State Machine Labels**: Track agent pending/working states
- **Stage Labels**: Indicate current pipeline stage
- **Quality Labels**: Mark quality gate status
- **Checkpoint Labels**: Record completion of agent milestones
- **Agent Activity Labels**: Show which agents are actively working
- **Control Labels**: Circuit breakers and manual overrides

## Quick Setup

### Option 1: Automated Script (Recommended)

Run the setup script to create all labels at once:

```bash
# From repository root
./scripts/setup-labels.sh
```

To update existing labels:

```bash
./scripts/setup-labels.sh --force
```

**Prerequisites:**
- GitHub CLI (`gh`) installed and authenticated
- Repository write permissions

### Option 2: Manual Creation

Use the GitHub CLI commands from the issue description, or manually create labels through the GitHub UI using the definitions in `labels.yml`.

### Option 3: Workflow-Based Sync

Use a GitHub Action to automatically sync labels from `labels.yml`. Popular options include:

- [EndBug/label-sync](https://github.com/EndBug/label-sync)
- [micnncim/action-label-syncer](https://github.com/micnncim/action-label-syncer)

## Label Categories

**Note on Label Usage:** This system includes both labels currently used by existing workflows (marked with ✅ below) and labels reserved for future state machine enhancements and automation features. All labels are defined now to ensure consistency and enable seamless integration as new features are added.

### Core Pipeline Labels

| Label | Description | Color | Used By | Status |
|-------|-------------|-------|---------|--------|
| `somas:dev` | Trigger autonomous pipeline | 🟢 0E8A16 | somas-orchestrator.yml | ✅ Active |
| `somas-project` | New SOMAS project | 🔵 1D76DB | somas-pipeline.yml | ✅ Active |

### Triage Labels

| Label | Description | Color | Used By | Status |
|-------|-------------|-------|----------|--------|
| `somas:change` | Change request | 🟡 FBCA04 | somas-orchestrator.yml (triage) | ✅ Active |
| `somas:enhance` | Enhancement suggestion | 🔵 A2EEEF | somas-orchestrator.yml (triage) | ✅ Active |
| `somas:question` | Question/research | 🟣 D876E3 | somas-orchestrator.yml (triage) | ✅ Active |
| `somas:bug` | Bug report | 🔴 D73A4A | somas-orchestrator.yml (triage) | ✅ Active |
| `somas:triaged` | Triaged by automation | 🟢 C2E0C6 | somas-orchestrator.yml (triage) | ✅ Active |

### State Machine Labels

**Status:** 🔮 Reserved for future state machine orchestration features

Track which agent is pending or in progress:

- `state:pending-planner`
- `state:pending-specifier`
- `state:pending-simulator`
- `state:pending-architect`
- `state:pending-implementer`
- `state:pending-tester`
- `state:pending-deployer`
- `state:complete`

All use color 🔵 BFDADC except `state:complete` which uses C5DEF5.

**Note:** These labels are defined now for future label-driven state machine transitions. Workflows can reference them once state machine features are implemented.

### Stage Labels

| Label | Description | Color | Used By | Status |
|-------|-------------|-------|---------|--------|
| `stage:*` (7 labels) | Track pipeline stage | 🔴 E99695 | somas-project-sync.yml, sync-stage-milestones.yml | ✅ Active |

Track the current pipeline stage:

- `stage:ideation`
- `stage:specification`
- `stage:simulation`
- `stage:architecture`
- `stage:implementation`
- `stage:validation`
- `stage:staging`

All use color 🔴 E99695.

Referenced by:
- `somas-project-sync.yml` for dynamic stage tracking
- `sync-stage-milestones.yml` for automatic milestone creation and assignment

### Quality Labels

**Status:** 🔮 Reserved for future quality gate automation

| Label | Description | Color |
|-------|-------------|-------|
| `quality:blocked` | Blocked by quality gate | 🟡 E4E669 |
| `quality:passed` | Quality gate passed | 🟢 C2E0C6 |
| `quality:review-needed` | Manual review needed | 🟡 FBCA04 |

### Checkpoint Labels

**Status:** 🔮 Reserved for future checkpoint automation

Mark completion of agent milestones:

- `checkpoint:planner-complete`
- `checkpoint:specifier-complete`
- `checkpoint:simulator-complete`
- `checkpoint:architect-complete`
- `checkpoint:implementer-complete`
- `checkpoint:tester-complete`
- `checkpoint:deployer-complete`

All use color 🟡 E4E669.

**Note:** These labels will be used for automatic milestone tracking once checkpoint features are implemented.

### Agent Activity Labels

**Status:** 🔮 Reserved for future agent status tracking

Show which agents are actively working:

- `agent:planner-working`
- `agent:specifier-working`
- `agent:simulator-working`
- `agent:architect-working`
- `agent:implementer-working`
- `agent:tester-working`
- `agent:deployer-working`

All use color 🔵 C5DEF5.

**Note:** These labels will enable real-time agent activity visualization in future releases.

### Control Labels

| Label | Description | Color | Purpose | Status |
|-------|-------------|-------|---------|--------|
| `somas:circuit-breaker` | Disable automation | 🔴 D73A4A | Emergency stop | ✅ Active |
| `somas:manual` | Manual intervention | 🟡 FBCA04 | Pause automation | 🔮 Reserved |
| `somas:retry` | Retry current stage | 🟡 FBCA04 | Recover from failure | 🔮 Reserved |

### Additional Workflow Labels

| Label | Description | Color | Status |
|-------|-------------|-------|--------|
| `somas:system` | SOMAS system changes | 🔵 1D76DB | 🔮 Reserved |
| `needs-human-review` | Human review required | 🟡 FBCA04 | 🔮 Reserved |
| `auto-merge-approved` | Auto-merge approved | 🟢 C2E0C6 | 🔮 Reserved |
| `somas:ready-for-review` | PR ready for review | 🟢 0E8A16 | ✅ Active |
| `somas-generated` | SOMAS-generated content | 🔵 1D76DB | ✅ Active |

## Label Status Key

- ✅ **Active**: Currently used by existing workflows
- 🔮 **Reserved**: Defined for future features and state machine enhancements

## Label Usage in Workflows

### somas-orchestrator.yml

Uses these labels for orchestration:
- `somas:dev` - Triggers autonomous pipeline
- `somas:change`, `somas:enhance`, `somas:question`, `somas:bug` - Triage routing
- `somas:triaged` - Marks completed triage
- `somas:circuit-breaker` - Disables automation

### somas-pipeline.yml

Uses these labels:
- `somas-project` - Triggers project initialization
- `somas:dev` - Applied automatically to new projects

### somas-project-sync.yml

Uses these labels:
- `stage:*` - Syncs project stage with issue labels

### sync-stage-milestones.yml

Automatically creates and assigns milestones based on stage labels:
- `stage:ideation` → Creates/assigns "Ideation" milestone
- `stage:specification` → Creates/assigns "Specification" milestone
- `stage:simulation` → Creates/assigns "Simulation" milestone
- `stage:architecture` → Creates/assigns "Architecture" milestone
- `stage:implementation` → Creates/assigns "Implementation" milestone
- `stage:validation` → Creates/assigns "Validation" milestone
- `stage:staging` → Creates/assigns "Staging" milestone

**Features:**
- Automatically creates milestones if they don't exist
- Assigns issue/PR to appropriate milestone when stage label is added
- Enforces one milestone per issue/PR (latest label wins)
- Removes milestone when the last `stage:*` label is removed; if other `stage:*` labels remain, the existing milestone is left unchanged
- Enables milestone-based progress tracking, burndown charts, and filtering
- Supports future expansion for version/release milestones

## Label Management Best Practices

### When to Add New Labels

Consider adding new labels when:
- Introducing new pipeline stages
- Adding new agent types
- Implementing new quality gates
- Creating new state machine transitions

### Label Naming Conventions

Follow these conventions for consistency:
- **Namespace prefix**: `somas:`, `state:`, `stage:`, `checkpoint:`, `agent:`, `quality:`
- **Lowercase**: Use lowercase for all label names
- **Hyphens**: Separate words with hyphens (e.g., `pending-planner`)
- **Descriptive**: Use clear, unambiguous names

### Updating Labels

To update label descriptions or colors:

1. Edit `.github/labels.yml`
2. Run `./scripts/setup-labels.sh --force`
3. Commit changes to repository

### Removing Deprecated Labels

To remove unused labels:

```bash
gh label delete "label-name"
```

Or use the GitHub web interface: Repository → Labels → Delete

## Troubleshooting

### Script Won't Run

**Issue**: Permission denied when running script  
**Solution**: Make script executable: `chmod +x scripts/setup-labels.sh`

**Issue**: `gh` command not found  
**Solution**: Install GitHub CLI from https://cli.github.com/

**Issue**: Not authenticated  
**Solution**: Run `gh auth login` and follow prompts

### Labels Already Exist

**Issue**: Script says labels already exist  
**Solution**: Run with `--force` flag to update: `./scripts/setup-labels.sh --force`

### Wrong Repository

**Issue**: Labels created in wrong repository  
**Solution**: Check current directory and ensure you're in the correct repository

### Missing Permissions

**Issue**: Cannot create labels - permission denied  
**Solution**: Ensure you have write access to the repository

## Integration with Future Features

This label system is designed to support:

- **Label-driven state machines**: Future workflows can trigger based on label changes
- **Visual pipeline tracking**: Labels provide real-time status in GitHub UI
- **Automated routing**: Triage labels enable intelligent request routing
- **Quality gates**: Quality labels enable automated decision points
- **Audit trails**: Label history provides execution forensics

## References

- **Configuration**: `.github/labels.yml` - Complete label definitions
- **Setup Script**: `scripts/setup-labels.sh` - Automated setup
- **Workflows**: `.github/workflows/` - Label usage examples
- **Documentation**: `docs/somas/README.md` - SOMAS system overview

## Contributing

When adding new labels:

1. Add definition to `.github/labels.yml`
2. Update this README with the new label
3. Document which workflows use it
4. Test with `./scripts/setup-labels.sh`
5. Commit all changes together

## Support

For issues with label setup:
- Check [Troubleshooting](#troubleshooting) section
- Review workflow configurations in `.github/workflows/`
- Consult SOMAS documentation in `docs/somas/`
- Open an issue with `somas:question` label
