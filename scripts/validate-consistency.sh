#!/bin/bash
# SOMAS Cross-Reference Validation Script
# @copilot-context: Validates consistency of references across the repository
# Ensures that changes in one area are reflected throughout the codebase
#
# This script checks:
# - Configuration files are valid YAML/JSON
# - Agent configurations referenced in workflows match actual files
# - Agent count consistency (actual files vs DEVELOPMENT_PLAN.md documentation)
# - Skills referenced in skill-rules.json exist
# - Templates referenced by agents exist
# - Documentation cross-references are valid
# - Workflow file references are valid
# - Python dependencies are properly formatted

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
ERRORS=0
WARNINGS=0

echo -e "${BLUE}🔍 SOMAS Cross-Reference Validation${NC}"
echo "======================================"
echo ""

# Function to report errors
error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
    ((ERRORS++))
}

# Function to report warnings
warning() {
    echo -e "${YELLOW}⚠️  WARNING: $1${NC}"
    ((WARNINGS++))
}

# Function to report success
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Function to check if file exists
check_file_exists() {
    local file="$1"
    local description="$2"

    if [[ ! -f "$REPO_ROOT/$file" ]]; then
        error "$description: $file does not exist"
        return 1
    else
        return 0
    fi
}

# Function to validate YAML syntax
validate_yaml() {
    local file="$1"
    local description="$2"

    if ! python3 -c "import yaml; yaml.safe_load(open('$REPO_ROOT/$file'))" 2>/dev/null; then
        error "$description: Invalid YAML syntax in $file"
        return 1
    else
        return 0
    fi
}

# Function to validate JSON syntax
validate_json() {
    local file="$1"
    local description="$2"

    if ! python3 -m json.tool "$REPO_ROOT/$file" >/dev/null 2>&1; then
        error "$description: Invalid JSON syntax in $file"
        return 1
    else
        return 0
    fi
}

echo "1. Validating Configuration Files..."
echo "-----------------------------------"

# Check main configuration file
if check_file_exists ".somas/config.yml" "Main configuration file"; then
    validate_yaml ".somas/config.yml" "Main configuration"
fi

# Check skill rules
if check_file_exists "skill-rules.json" "Skill rules configuration"; then
    validate_json "skill-rules.json" "Skill rules"
fi

# Check retrieval configuration
if check_file_exists "retrieval.yml" "Retrieval configuration"; then
    validate_yaml "retrieval.yml" "Retrieval configuration"
fi

echo ""
echo "2. Validating Agent Configurations..."
echo "-----------------------------------"

# Get list of agents referenced in config.yml
if [[ -f "$REPO_ROOT/.somas/config.yml" ]]; then
    REFERENCED_AGENTS=$(python3 -c "
import yaml
with open('$REPO_ROOT/.somas/config.yml') as f:
    config = yaml.safe_load(f)
agents = set()
for stage in config.get('pipeline', {}).get('stages', []):
    if 'agent' in stage:
        agents.add(stage['agent'])
    if 'secondary_agent' in stage:
        agents.add(stage['secondary_agent'])
    if 'secondary_agents' in stage:
        agents.update(stage['secondary_agents'])
    if 'config_file' in stage:
        # Extract agent name from config file path
        import os
        config_file = stage['config_file']
        if config_file.startswith('.somas/agents/') and config_file.endswith('.yml'):
            agent_name = os.path.basename(config_file).replace('.yml', '')
            agents.add(agent_name)
print('\n'.join(sorted(agents)))
" 2>/dev/null || echo "")

    # Check each referenced agent has a config file
    while IFS= read -r agent; do
        if [[ -n "$agent" ]]; then
            agent_file=".somas/agents/${agent}.yml"
            if ! check_file_exists "$agent_file" "Agent configuration for '$agent'"; then
                continue
            fi
            validate_yaml "$agent_file" "Agent configuration for '$agent'"
        fi
    done <<< "$REFERENCED_AGENTS"
fi

echo ""
echo "3. Validating Agent Counts..."
echo "---------------------------"

# Count actual agent configuration files (excluding base templates)
if [[ -d "$REPO_ROOT/.somas/agents" ]]; then
    ACTUAL_AGENT_COUNT=$(find "$REPO_ROOT/.somas/agents" -maxdepth 1 -name "*.yml" -type f ! -name "_*.yml" | wc -l)

    # Count agents mentioned in DEVELOPMENT_PLAN.md
    if [[ -f "$REPO_ROOT/DEVELOPMENT_PLAN.md" ]]; then
        # Extract agent count claims from DEVELOPMENT_PLAN.md
        PLAN_AGENT_COUNTS=$(grep -o "[0-9]\+ agents\|[0-9]\+/[0-9]\+ agents" "$REPO_ROOT/DEVELOPMENT_PLAN.md" | head -5)

        # Count what we say we have: complete + minimal + critical gaps
        COMPLETE_AGENTS=$(grep -oP '\*\*[0-9]+ Complete Agents:\*\*' "$REPO_ROOT/DEVELOPMENT_PLAN.md" | grep -oP '[0-9]+' | head -1)
        MINIMAL_AGENTS=$(grep -oP '\*\*[0-9]+ Minimal Agents:\*\*' "$REPO_ROOT/DEVELOPMENT_PLAN.md" | grep -oP '[0-9]+' | head -1)
        CRITICAL_GAPS=$(grep -oP '\*\*[0-9]+ Critical Gaps:\*\*' "$REPO_ROOT/DEVELOPMENT_PLAN.md" | grep -oP '[0-9]+' | head -1)

        if [[ -n "$COMPLETE_AGENTS" && -n "$MINIMAL_AGENTS" && -n "$CRITICAL_GAPS" ]]; then
            DOCUMENTED_AGENT_COUNT=$((COMPLETE_AGENTS + MINIMAL_AGENTS + CRITICAL_GAPS))

            # Check if counts match
            if [[ "$ACTUAL_AGENT_COUNT" -eq "$DOCUMENTED_AGENT_COUNT" ]]; then
                success "Agent count consistent: $ACTUAL_AGENT_COUNT agents ($COMPLETE_AGENTS complete + $MINIMAL_AGENTS minimal + $CRITICAL_GAPS critical gaps)"
            else
                error "Agent count mismatch: File system has $ACTUAL_AGENT_COUNT agents (excluding templates), but DEVELOPMENT_PLAN.md documents $DOCUMENTED_AGENT_COUNT ($COMPLETE_AGENTS complete + $MINIMAL_AGENTS minimal + $CRITICAL_GAPS critical gaps)"
                echo "  Actual agents: $(find "$REPO_ROOT/.somas/agents" -maxdepth 1 -name "*.yml" -type f ! -name "_*.yml" -exec basename {} .yml \; | sort | paste -sd ',' -)"
            fi
        else
            warning "Could not parse agent counts from DEVELOPMENT_PLAN.md"
        fi
    else
        warning "DEVELOPMENT_PLAN.md not found, skipping agent count verification"
    fi
else
    error "Agent configuration directory not found: .somas/agents"
fi

echo ""
echo "4. Validating Skill References..."
echo "-------------------------------"

# Check skills referenced in skill-rules.json exist
if [[ -f "$REPO_ROOT/skill-rules.json" ]]; then
    REFERENCED_SKILLS=$(python3 -c "
import json
with open('$REPO_ROOT/skill-rules.json') as f:
    config = json.load(f)
skills = set()
for skill in config.get('skills', []):
    skills.add(skill['name'])
print('\n'.join(sorted(skills)))
" 2>/dev/null || echo "")

    # Check each referenced skill exists
    while IFS= read -r skill; do
        if [[ -n "$skill" ]]; then
            # Map skill names to directory and file names
            case "$skill" in
                "AgentDesign") 
                    skill_dir="skills/agent-design"
                    main_file="agent-design-main.md"
                    ;;
                "PromptOptimization") 
                    skill_dir="skills/prompt-optimization"
                    main_file="prompt-optimization-main.md"
                    ;;
                "AutonomousSystems") 
                    skill_dir="skills/autonomous-systems"
                    main_file="autonomous-systems-main.md"
                    ;;
                *) 
                    skill_dir="skills/$(echo "$skill" | tr '[:upper:]' '[:lower:]')"
                    main_file="main.md"
                    ;;
            esac
            
            if ! check_file_exists "$skill_dir/$main_file" "Skill documentation for '$skill'"; then
                continue
            fi
            if ! check_file_exists "$skill_dir/patterns.json" "Skill patterns for '$skill'"; then
                continue
            fi
            validate_json "$skill_dir/patterns.json" "Skill patterns for '$skill'"
        fi
    done <<< "$REFERENCED_SKILLS"
fi

echo ""
echo "5. Validating Template References..."
echo "----------------------------------"

# Check templates referenced by agents exist
if [[ -d "$REPO_ROOT/.somas/templates" ]]; then
    # Find all template references in agent configs
    # Check for known template references manually
    for template in "architecture.md" "plan.md" "SPEC.md" "execution_plan.md"; do
        template_file=".somas/templates/$template"
        check_file_exists "$template_file" "Template referenced by agents"
    done
fi

echo ""
echo "6. Validating Documentation Cross-References..."
echo "----------------------------------------------"

# Check internal documentation links in README files
# This is a basic check - could be expanded with more sophisticated link checking
if [[ -f "$REPO_ROOT/README.md" ]]; then
    # Check for broken relative links (basic check)
    BROKEN_LINKS=$(grep -n "\[.*\](\.\." "$REPO_ROOT/README.md" | head -5 || echo "")
    if [[ -n "$BROKEN_LINKS" ]]; then
        warning "Found relative links in README.md that may need verification"
    fi
fi

echo ""
echo "7. Validating Workflow Dependencies..."
echo "------------------------------------"

# Check that workflows reference existing files
WORKFLOW_FILES=$(find "$REPO_ROOT/.github/workflows" -name "*.yml" -type f 2>/dev/null || echo "")

for workflow in $WORKFLOW_FILES; do
    workflow_name=$(basename "$workflow" .yml)

    # Check for references to .somas files
    SOMAS_REFS=$(grep -o "\.somas/[^\"']*" "$workflow" 2>/dev/null | tr ' ' '\n' | sort | uniq || echo "")

    while IFS= read -r ref; do
        if [[ -n "$ref" && "$ref" != ".somas/" ]]; then
            # Skip dynamic paths with variables or wildcards
            if [[ "$ref" == *"\${"* || "$ref" == *"*"* ]]; then
                continue
            fi
            # Remove trailing punctuation and check if file exists
            clean_ref=$(echo "$ref" | sed 's/[[:punct:]]*$//')
            if [[ "$clean_ref" == *.yml || "$clean_ref" == *.md || "$clean_ref" == *.json ]]; then
                check_file_exists "$clean_ref" "File referenced in workflow $workflow_name"
            fi
        fi
    done <<< "$SOMAS_REFS"
done

echo ""
echo "8. Validating Python Dependencies..."
echo "----------------------------------"

# Check requirements.txt syntax
if [[ -f "$REPO_ROOT/requirements.txt" ]]; then
    # Basic syntax check - ensure each line is valid
    while IFS= read -r line; do
        # Skip comments and empty lines
        [[ "$line" =~ ^[[:space:]]*# ]] && continue
        [[ -z "$line" ]] && continue

        # Check for basic package==version format
        if ! echo "$line" | grep -q "^[a-zA-Z0-9_-]\+[=<>!]\{0,2\}[0-9]" && \
           ! echo "$line" | grep -q "^[a-zA-Z0-9_-]\+$"; then
            warning "Potentially malformed dependency in requirements.txt: $line"
        fi
    done < "$REPO_ROOT/requirements.txt"
fi

echo ""
echo "======================================"
if [[ $ERRORS -eq 0 && $WARNINGS -eq 0 ]]; then
    success "All cross-references are valid!"
    exit 0
elif [[ $ERRORS -eq 0 ]]; then
    echo -e "${YELLOW}Validation completed with $WARNINGS warnings${NC}"
    exit 0
else
    echo -e "${RED}Validation failed with $ERRORS errors and $WARNINGS warnings${NC}"
    echo ""
    echo "Please fix the errors above before proceeding."
    exit 1
fi
