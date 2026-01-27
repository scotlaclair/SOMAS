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

# Note: set -e is NOT used to allow proper error handling per label

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

# Helper function to create labels with proper error handling
create_label() {
    local name="$1"
    local description="$2"
    local color="$3"
    local force="$4"
    
    # Capture output and exit code
    local output
    local exit_code
    output=$(gh label create "$name" --description "$description" --color "$color" --force="$force" 2>&1)
    exit_code=$?
    
    if [[ $exit_code -eq 0 ]]; then
        echo -e "  ${GREEN}✓${NC} $name"
        ((CREATED++))
        return 0
    else
        # Check if it's a "label already exists" error when not using force mode
        if [[ $exit_code -eq 1 ]] && [[ "$force" == "false" ]] && [[ "$output" == *"already exists"* ]]; then
            echo -e "  ${YELLOW}○${NC} $name (already exists)"
            ((SKIPPED++))
        else
            echo -e "  ${RED}✗${NC} $name (failed)"
            if [[ -n "$output" ]]; then
                echo "$output" | sed 's/^/    /' # Indent error message
            fi
            ((FAILED++))
        fi
        return $exit_code
    fi
}

# Core Pipeline Labels
echo -e "${YELLOW}[Core Pipeline Labels]${NC}"
create_label "somas:dev" "Trigger SOMAS autonomous pipeline in development mode" "0E8A16" "$FORCE_MODE"
create_label "somas-project" "New SOMAS project - triggers project initialization" "1D76DB" "$FORCE_MODE"

# Triage Labels
echo -e "\n${YELLOW}[Triage Labels]${NC}"
create_label "somas:change" "Change request - modification to existing functionality" "FBCA04" "$FORCE_MODE"
create_label "somas:enhance" "Enhancement suggestion - new feature or improvement" "A2EEEF" "$FORCE_MODE"
create_label "somas:question" "Question or research request" "D876E3" "$FORCE_MODE"
create_label "somas:bug" "Bug report - defect in existing functionality" "D73A4A" "$FORCE_MODE"
create_label "somas:triaged" "Request has been triaged by automation" "C2E0C6" "$FORCE_MODE"

# State Machine Labels
echo -e "\n${YELLOW}[State Machine Labels]${NC}"
create_label "state:pending-planner" "Planner agent is pending or in progress" "BFDADC" "$FORCE_MODE"
create_label "state:pending-specifier" "Specifier agent is pending or in progress" "BFDADC" "$FORCE_MODE"
create_label "state:pending-simulator" "Simulator agent is pending or in progress" "BFDADC" "$FORCE_MODE"
create_label "state:pending-architect" "Architect agent is pending or in progress" "BFDADC" "$FORCE_MODE"
create_label "state:pending-implementer" "Implementer agent is pending or in progress" "BFDADC" "$FORCE_MODE"
create_label "state:pending-tester" "Tester/validator agent is pending or in progress" "BFDADC" "$FORCE_MODE"
create_label "state:pending-deployer" "Deployer/staging agent is pending or in progress" "BFDADC" "$FORCE_MODE"
create_label "state:complete" "Pipeline execution complete - ready for review" "C5DEF5" "$FORCE_MODE"

# Stage Labels
echo -e "\n${YELLOW}[Stage Labels]${NC}"
create_label "stage:ideation" "Ideation stage - initial planning" "E99695" "$FORCE_MODE"
create_label "stage:specification" "Specification stage - requirements definition" "E99695" "$FORCE_MODE"
create_label "stage:simulation" "Simulation stage - Monte Carlo optimization" "E99695" "$FORCE_MODE"
create_label "stage:architecture" "Architecture stage - system design" "E99695" "$FORCE_MODE"
create_label "stage:implementation" "Implementation stage - code generation" "E99695" "$FORCE_MODE"
create_label "stage:validation" "Validation stage - testing and quality checks" "E99695" "$FORCE_MODE"
create_label "stage:staging" "Staging stage - deployment preparation" "E99695" "$FORCE_MODE"

# Quality Labels
echo -e "\n${YELLOW}[Quality Labels]${NC}"
create_label "quality:blocked" "Blocked by quality gate failure" "E4E669" "$FORCE_MODE"
create_label "quality:passed" "Quality gate passed successfully" "C2E0C6" "$FORCE_MODE"
create_label "quality:review-needed" "Manual quality review needed" "FBCA04" "$FORCE_MODE"

# Checkpoint Labels
echo -e "\n${YELLOW}[Checkpoint Labels]${NC}"
create_label "checkpoint:planner-complete" "Planner agent checkpoint reached" "E4E669" "$FORCE_MODE"
create_label "checkpoint:specifier-complete" "Specifier agent checkpoint reached" "E4E669" "$FORCE_MODE"
create_label "checkpoint:simulator-complete" "Simulator agent checkpoint reached" "E4E669" "$FORCE_MODE"
create_label "checkpoint:architect-complete" "Architect agent checkpoint reached" "E4E669" "$FORCE_MODE"
create_label "checkpoint:implementer-complete" "Implementer agent checkpoint reached" "E4E669" "$FORCE_MODE"
create_label "checkpoint:tester-complete" "Tester/validator agent checkpoint reached" "E4E669" "$FORCE_MODE"
create_label "checkpoint:deployer-complete" "Deployer agent checkpoint reached" "E4E669" "$FORCE_MODE"

# Agent Activity Labels
echo -e "\n${YELLOW}[Agent Activity Labels]${NC}"
create_label "agent:planner-working" "Planner agent is currently working" "C5DEF5" "$FORCE_MODE"
create_label "agent:specifier-working" "Specifier agent is currently working" "C5DEF5" "$FORCE_MODE"
create_label "agent:simulator-working" "Simulator agent is currently working" "C5DEF5" "$FORCE_MODE"
create_label "agent:architect-working" "Architect agent is currently working" "C5DEF5" "$FORCE_MODE"
create_label "agent:implementer-working" "Implementer agent is currently working" "C5DEF5" "$FORCE_MODE"
create_label "agent:tester-working" "Tester/validator agent is currently working" "C5DEF5" "$FORCE_MODE"
create_label "agent:deployer-working" "Deployer agent is currently working" "C5DEF5" "$FORCE_MODE"

# Circuit Breaker & Control Labels
echo -e "\n${YELLOW}[Circuit Breaker & Control Labels]${NC}"
create_label "somas:circuit-breaker" "Disable all SOMAS automation for this issue" "D73A4A" "$FORCE_MODE"
create_label "somas:manual" "Manual intervention mode - automation paused" "FBCA04" "$FORCE_MODE"
create_label "somas:retry" "Retry the current stage after failure" "FBCA04" "$FORCE_MODE"

# Additional Workflow Labels
echo -e "\n${YELLOW}[Additional Workflow Labels]${NC}"
create_label "somas:system" "Changes to SOMAS system files" "1D76DB" "$FORCE_MODE"
create_label "needs-human-review" "Requires human review before proceeding" "FBCA04" "$FORCE_MODE"
create_label "auto-merge-approved" "Approved for automatic merging in dev environment" "C2E0C6" "$FORCE_MODE"
create_label "somas:ready-for-review" "SOMAS-generated PR ready for human review" "0E8A16" "$FORCE_MODE"
create_label "somas-generated" "Content generated by SOMAS automation" "1D76DB" "$FORCE_MODE"

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
