#!/bin/bash
# SOMAS Label Setup Script
# 
# This script creates all standard SOMAS labels in the GitHub repository
# using the GitHub CLI (gh).
# 
# Prerequisites:
# - GitHub CLI (gh) installed and authenticated
# - Appropriate repository permissions
# 
# Usage:
#   ./scripts/setup-labels.sh [--force]
# 
# Options:
#   --force    Delete existing labels with the same name before creating
# 
# The script uses hardcoded label definitions (for portability) and creates
# them in the current repository, using .github/labels.yml as the reference
# specification for those labels.

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LABELS_FILE="$REPO_ROOT/.github/labels.yml"

FORCE_MODE=false
if [[ "$1" == "--force" ]]; then
    FORCE_MODE=true
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) is not installed.${NC}"
    echo "Please install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${RED}Error: Not authenticated with GitHub CLI.${NC}"
    echo "Please run: gh auth login"
    exit 1
fi

# Check if labels.yml exists
if [[ ! -f "$LABELS_FILE" ]]; then
    echo -e "${RED}Error: Labels file not found at $LABELS_FILE${NC}"
    exit 1
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}SOMAS Label Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Repository: ${GREEN}$(gh repo view --json nameWithOwner -q .nameWithOwner)${NC}"
echo -e "Labels file: $LABELS_FILE"
echo -e "Force mode: $FORCE_MODE"
echo ""

# Parse YAML and create labels
# Note: Labels are hardcoded below for simplicity and portability.
# For dynamic YAML parsing, consider using yq or a Python script.
echo -e "${BLUE}Creating labels...${NC}"
echo ""

CREATED=0
SKIPPED=0
FAILED=0

# Core Pipeline Labels
echo -e "${YELLOW}[Core Pipeline Labels]${NC}"
gh label create "somas:dev" --description "Trigger SOMAS autonomous pipeline in development mode" --color "0E8A16" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} somas:dev" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} somas:dev (already exists)" && ((SKIPPED++)); }
gh label create "somas-project" --description "New SOMAS project - triggers project initialization" --color "1D76DB" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} somas-project" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} somas-project (already exists)" && ((SKIPPED++)); }

# Triage Labels
echo -e "\n${YELLOW}[Triage Labels]${NC}"
gh label create "somas:change" --description "Change request - modification to existing functionality" --color "FBCA04" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} somas:change" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} somas:change (already exists)" && ((SKIPPED++)); }
gh label create "somas:enhance" --description "Enhancement suggestion - new feature or improvement" --color "A2EEEF" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} somas:enhance" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} somas:enhance (already exists)" && ((SKIPPED++)); }
gh label create "somas:question" --description "Question or research request" --color "D876E3" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} somas:question" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} somas:question (already exists)" && ((SKIPPED++)); }
gh label create "somas:bug" --description "Bug report - defect in existing functionality" --color "D73A4A" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} somas:bug" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} somas:bug (already exists)" && ((SKIPPED++)); }
gh label create "somas:triaged" --description "Request has been triaged by automation" --color "C2E0C6" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} somas:triaged" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} somas:triaged (already exists)" && ((SKIPPED++)); }

# State Machine Labels
echo -e "\n${YELLOW}[State Machine Labels]${NC}"
gh label create "state:pending-planner" --description "Planner agent is pending or in progress" --color "BFDADC" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} state:pending-planner" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} state:pending-planner (already exists)" && ((SKIPPED++)); }
gh label create "state:pending-specifier" --description "Specifier agent is pending or in progress" --color "BFDADC" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} state:pending-specifier" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} state:pending-specifier (already exists)" && ((SKIPPED++)); }
gh label create "state:pending-simulator" --description "Simulator agent is pending or in progress" --color "BFDADC" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} state:pending-simulator" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} state:pending-simulator (already exists)" && ((SKIPPED++)); }
gh label create "state:pending-architect" --description "Architect agent is pending or in progress" --color "BFDADC" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} state:pending-architect" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} state:pending-architect (already exists)" && ((SKIPPED++)); }
gh label create "state:pending-implementer" --description "Implementer agent is pending or in progress" --color "BFDADC" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} state:pending-implementer" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} state:pending-implementer (already exists)" && ((SKIPPED++)); }
gh label create "state:pending-tester" --description "Tester/validator agent is pending or in progress" --color "BFDADC" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} state:pending-tester" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} state:pending-tester (already exists)" && ((SKIPPED++)); }
gh label create "state:pending-deployer" --description "Deployer/staging agent is pending or in progress" --color "BFDADC" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} state:pending-deployer" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} state:pending-deployer (already exists)" && ((SKIPPED++)); }
gh label create "state:complete" --description "Pipeline execution complete - ready for review" --color "C5DEF5" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} state:complete" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} state:complete (already exists)" && ((SKIPPED++)); }

# Stage Labels
echo -e "\n${YELLOW}[Stage Labels]${NC}"
gh label create "stage:ideation" --description "Ideation stage - initial planning" --color "E99695" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} stage:ideation" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} stage:ideation (already exists)" && ((SKIPPED++)); }
gh label create "stage:specification" --description "Specification stage - requirements definition" --color "E99695" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} stage:specification" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} stage:specification (already exists)" && ((SKIPPED++)); }
gh label create "stage:simulation" --description "Simulation stage - Monte Carlo optimization" --color "E99695" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} stage:simulation" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} stage:simulation (already exists)" && ((SKIPPED++)); }
gh label create "stage:architecture" --description "Architecture stage - system design" --color "E99695" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} stage:architecture" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} stage:architecture (already exists)" && ((SKIPPED++)); }
gh label create "stage:implementation" --description "Implementation stage - code generation" --color "E99695" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} stage:implementation" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} stage:implementation (already exists)" && ((SKIPPED++)); }
gh label create "stage:validation" --description "Validation stage - testing and quality checks" --color "E99695" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} stage:validation" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} stage:validation (already exists)" && ((SKIPPED++)); }
gh label create "stage:staging" --description "Staging stage - deployment preparation" --color "E99695" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} stage:staging" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} stage:staging (already exists)" && ((SKIPPED++)); }

# Quality Labels
echo -e "\n${YELLOW}[Quality Labels]${NC}"
gh label create "quality:blocked" --description "Blocked by quality gate failure" --color "E4E669" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} quality:blocked" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} quality:blocked (already exists)" && ((SKIPPED++)); }
gh label create "quality:passed" --description "Quality gate passed successfully" --color "C2E0C6" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} quality:passed" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} quality:passed (already exists)" && ((SKIPPED++)); }
gh label create "quality:review-needed" --description "Manual quality review needed" --color "FBCA04" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} quality:review-needed" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} quality:review-needed (already exists)" && ((SKIPPED++)); }

# Checkpoint Labels
echo -e "\n${YELLOW}[Checkpoint Labels]${NC}"
gh label create "checkpoint:planner-complete" --description "Planner agent checkpoint reached" --color "E4E669" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} checkpoint:planner-complete" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} checkpoint:planner-complete (already exists)" && ((SKIPPED++)); }
gh label create "checkpoint:specifier-complete" --description "Specifier agent checkpoint reached" --color "E4E669" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} checkpoint:specifier-complete" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} checkpoint:specifier-complete (already exists)" && ((SKIPPED++)); }
gh label create "checkpoint:simulator-complete" --description "Simulator agent checkpoint reached" --color "E4E669" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} checkpoint:simulator-complete" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} checkpoint:simulator-complete (already exists)" && ((SKIPPED++)); }
gh label create "checkpoint:architect-complete" --description "Architect agent checkpoint reached" --color "E4E669" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} checkpoint:architect-complete" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} checkpoint:architect-complete (already exists)" && ((SKIPPED++)); }
gh label create "checkpoint:implementer-complete" --description "Implementer agent checkpoint reached" --color "E4E669" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} checkpoint:implementer-complete" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} checkpoint:implementer-complete (already exists)" && ((SKIPPED++)); }
gh label create "checkpoint:tester-complete" --description "Tester/validator agent checkpoint reached" --color "E4E669" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} checkpoint:tester-complete" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} checkpoint:tester-complete (already exists)" && ((SKIPPED++)); }
gh label create "checkpoint:deployer-complete" --description "Deployer agent checkpoint reached" --color "E4E669" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} checkpoint:deployer-complete" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} checkpoint:deployer-complete (already exists)" && ((SKIPPED++)); }

# Agent Activity Labels
echo -e "\n${YELLOW}[Agent Activity Labels]${NC}"
gh label create "agent:planner-working" --description "Planner agent is currently working" --color "C5DEF5" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} agent:planner-working" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} agent:planner-working (already exists)" && ((SKIPPED++)); }
gh label create "agent:specifier-working" --description "Specifier agent is currently working" --color "C5DEF5" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} agent:specifier-working" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} agent:specifier-working (already exists)" && ((SKIPPED++)); }
gh label create "agent:simulator-working" --description "Simulator agent is currently working" --color "C5DEF5" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} agent:simulator-working" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} agent:simulator-working (already exists)" && ((SKIPPED++)); }
gh label create "agent:architect-working" --description "Architect agent is currently working" --color "C5DEF5" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} agent:architect-working" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} agent:architect-working (already exists)" && ((SKIPPED++)); }
gh label create "agent:implementer-working" --description "Implementer agent is currently working" --color "C5DEF5" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} agent:implementer-working" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} agent:implementer-working (already exists)" && ((SKIPPED++)); }
gh label create "agent:tester-working" --description "Tester/validator agent is currently working" --color "C5DEF5" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} agent:tester-working" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} agent:tester-working (already exists)" && ((SKIPPED++)); }
gh label create "agent:deployer-working" --description "Deployer agent is currently working" --color "C5DEF5" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} agent:deployer-working" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} agent:deployer-working (already exists)" && ((SKIPPED++)); }

# Circuit Breaker & Control Labels
echo -e "\n${YELLOW}[Circuit Breaker & Control Labels]${NC}"
gh label create "somas:circuit-breaker" --description "Disable all SOMAS automation for this issue" --color "D73A4A" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} somas:circuit-breaker" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} somas:circuit-breaker (already exists)" && ((SKIPPED++)); }
gh label create "somas:manual" --description "Manual intervention mode - automation paused" --color "FBCA04" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} somas:manual" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} somas:manual (already exists)" && ((SKIPPED++)); }
gh label create "somas:retry" --description "Retry the current stage after failure" --color "FBCA04" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} somas:retry" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} somas:retry (already exists)" && ((SKIPPED++)); }

# Additional Workflow Labels
echo -e "\n${YELLOW}[Additional Workflow Labels]${NC}"
gh label create "somas:system" --description "Changes to SOMAS system files" --color "1D76DB" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} somas:system" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} somas:system (already exists)" && ((SKIPPED++)); }
gh label create "needs-human-review" --description "Requires human review before proceeding" --color "FBCA04" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} needs-human-review" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} needs-human-review (already exists)" && ((SKIPPED++)); }
gh label create "auto-merge-approved" --description "Approved for automatic merging in dev environment" --color "C2E0C6" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} auto-merge-approved" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} auto-merge-approved (already exists)" && ((SKIPPED++)); }
gh label create "somas:ready-for-review" --description "SOMAS-generated PR ready for human review" --color "0E8A16" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} somas:ready-for-review" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} somas:ready-for-review (already exists)" && ((SKIPPED++)); }
gh label create "somas-generated" --description "Content generated by SOMAS automation" --color "1D76DB" --force=$FORCE_MODE 2>/dev/null && echo -e "  ${GREEN}✓${NC} somas-generated" && ((CREATED++)) || { echo -e "  ${YELLOW}○${NC} somas-generated (already exists)" && ((SKIPPED++)); }

# Summary
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Created:${NC} $CREATED labels"
echo -e "${YELLOW}Skipped:${NC} $SKIPPED labels (already existed)"
if [[ $FAILED -gt 0 ]]; then
    echo -e "${RED}Failed:${NC} $FAILED labels"
fi
echo ""
echo -e "${GREEN}✓ Label setup complete!${NC}"
echo ""
echo "View all labels at: $(gh repo view --json url -q .url)/labels"
