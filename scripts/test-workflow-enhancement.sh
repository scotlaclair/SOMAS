#!/usr/bin/env bash
#
# test-workflow-enhancement.sh
# Test SOMAS workflow with an enhancement submission

set -euo pipefail

# Load helper functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/workflow-test-helpers.sh
source "${SCRIPT_DIR}/lib/workflow-test-helpers.sh"

# Configuration
TEST_NAME="Enhancement Workflow"
PROJECT_TITLE="[TEST] Enhancement: Add scientific calculator functions"
ENHANCEMENT_TYPE="feature_idea"
PRIORITY="medium"

# Main test function
main() {
    local start_time
    start_time=$(date +%s)
    
    local test_status="FAILED"
    local issue_number=""
    
    trap 'print_summary "${TEST_NAME}" "${test_status}" "$(($(date +%s) - start_time))"' EXIT
    
    init_log "${TEST_NAME}"
    log_section "SOMAS Workflow Test: Enhancement"
    
    # Prerequisites
    check_requirements || exit 1
    check_gh_auth || exit 1
    
    # Create enhancement issue
    log_section "Step 1: Create Enhancement Issue"
    
    local issue_body
    issue_body=$(cat <<EOF
### Enhancement Type

${ENHANCEMENT_TYPE}

### Description

Add scientific calculator functions including:
- Trigonometric functions (sin, cos, tan)
- Logarithmic functions (log, ln)
- Exponentiation and roots
- Constants (π, e)

### Priority Level

${PRIORITY}

### Use Cases

1. Students performing scientific calculations
2. Engineers needing quick calculations
3. Data scientists doing mathematical operations

### Benefits

- Extends calculator functionality
- Makes it more useful for technical users
- Competitive with other calculator applications

### Technical Requirements

- Implement using Python math library
- Add comprehensive tests for each function
- Update documentation with examples
- Maintain backward compatibility

### Additional Context

This is a test enhancement request for SOMAS workflow validation.
EOF
)
    
    issue_number=$(create_issue "${PROJECT_TITLE}" "${issue_body}" "somas:enhance")
    
    if [ -z "${issue_number}" ]; then
        log_error "Failed to create issue"
        exit 1
    fi
    
    # Monitor workflows
    log_section "Step 2: Monitor Workflows"
    
    local intake_run_id
    if intake_run_id=$(wait_for_workflow_trigger "intake-triage.yml" "${issue_number}" 60); then
        monitor_workflow "${intake_run_id}" 30 || log_warning "Intake workflow had issues"
    fi
    
    # Verify triage
    log_section "Step 3: Verify Enhancement Triage"
    
    sleep 15
    check_issue_labels "${issue_number}" "somas:enhance" || log_warning "Enhancement label not applied"
    check_issue_comments "${issue_number}" "enhancement" || log_warning "Enhancement triage comment not found"
    
    test_status="PASSED"
    log_success "Enhancement workflow test completed"
}

main "$@"
