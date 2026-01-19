# Merge Conflict Resolution Guide for PR #1

## Problem Analysis

PR #1 (`copilot/initialize-somas-lite-pipeline`) is attempting to merge into `main`, but the branches have diverged significantly:

### PR #1 Branch (SOMAS Lite)
- **Commit**: 68693ac44d804b5b989af9655044b63fd99d41d1
- **Implementation**: 5-stage autonomous pipeline with 8 AI agents
- **Key Components**:
  - `.github/workflows/somas-pipeline.yml` (16,991 bytes)
  - 8 agent configurations in `.somas/agents/`
  - Comprehensive documentation for each agent
  - Templates for plans and architecture
  - Design patterns guide
  - Getting started tutorial

###  Main Branch (SOMAS with Specification Stage)
- **Commit**: 725f7b0ed0b02e783fc11e4fbf6012448901b6cc
- **Implementation**: 7-stage specification-driven pipeline with simulation
- **Key Components**:
  - `.github/workflows/somas-pipeline.yml` (different version)
  - `.github/workflows/somas-project-sync.yml` (additional workflow)
  - Simulator and specifier agents
  - GitHub Project integration
  - Security fixes and improvements from PR #2, #4, and #5

## Conflict Nature

The branches represent **two parallel implementations** of SOMAS:
1. **SOMAS Lite** (PR #1): Original vision with 5 stages and comprehensive agent system
2. **SOMAS Extended** (main): Enhanced with specification stage, simulation, and project management

## Resolution Strategy

Since both implementations have value, the recommended approach is to **merge both implementations** so they can coexist:

### Option 1: Keep Both Implementations (Recommended)

Merge the branches while preserving both implementations:

1. **Workflow Files**: Keep both workflows
   - Rename PR #1's `somas-pipeline.yml` to `somas-lite-pipeline.yml`
   - Keep main's `somas-pipeline.yml` and `somas-project-sync.yml`
   - Each can be triggered by different labels

2. **Agent Configurations**: Merge both agent sets
   - Keep all agent configs from both branches
   - PR #1 has: planner, architect, implementer, tester, reviewer, security, documenter, orchestrator
   - Main has: simulator, specifier
   - All can coexist in `.somas/agents/`

3. **Documentation**: Merge and enhance
   - Combine README content to document both modes
   - Keep all documentation from both branches
   - Add a section explaining the two operational modes

4. **Templates**: Keep all templates from both branches

### Option 2: Replace with PR #1 (Alternative)

If the decision is to revert to SOMAS Lite:

1. Use PR #1's implementation as the base
2. Cherry-pick security fixes from main (commits from PR #4 and #5)
3. This would lose the specification stage and simulation features

### Option 3: Keep Main, Close PR #1 (Alternative)

Simply close PR #1 and continue with the current main implementation.

## Recommended Manual Steps

To implement Option 1 (recommended), someone with repository access should:

```bash
# Clone the repository
git clone https://github.com/scotlaclair/SOMAS.git
cd SOMAS

# Checkout PR #1 branch
git checkout copilot/initialize-somas-lite-pipeline

# Create a new branch for the merge
git checkout -b merge-somas-lite-and-main

# Merge main into this branch
git merge main

# Resolve conflicts:
# 1. Rename .github/workflows/somas-pipeline.yml to somas-lite-pipeline.yml
git mv .github/workflows/somas-pipeline.yml .github/workflows/somas-lite-pipeline.yml

# 2. Checkout main's workflows
git checkout main -- .github/workflows/somas-pipeline.yml
git checkout main -- .github/workflows/somas-project-sync.yml

# 3. For conflicting files, manually merge or keep both versions

# 4. Merge README files
# Edit README.md to include content from both versions

# 5. Keep all agent configs from both branches
# They should not conflict as they have different names

# Commit the resolution
git add .
git commit -m "Merge SOMAS Lite and SOMAS Extended implementations"

# Push to PR #1 branch
git push origin merge-somas-lite-and-main:copilot/initialize-somas-lite-pipeline --force
```

## Implementation via This Branch

Since I'm on `copilot/resolve-merge-conflicts`, I can implement the resolution here, but I need to fetch content from both branches via the GitHub API since git authentication is unavailable in this environment.

## Next Steps

1. Decide which resolution option to pursue
2. Implement the chosen strategy
3. Test that workflows are valid YAML
4. Update PR #1 to resolve conflicts
5. Review and merge

## Files That Need Attention

1. **README.md** - Needs content from both branches
2. **workflows/somas-pipeline.yml** - Exists in both, needs rename or merge
3. **.somas/config.yml** - May have differences
4. **docs/** - May have overlapping documentation

