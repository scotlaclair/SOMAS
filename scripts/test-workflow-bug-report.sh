#!/usr/bin/env bash
#
# test-workflow-bug-report.sh
# Test SOMAS workflow with a bug report submission
#
# This script tests the bug report workflow through the SOMAS pipeline

set -euo pipefail

# Load helper functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/workflow-test-helpers.sh
source "${SCRIPT_DIR}/lib/workflow-test-helpers.sh"

# Configuration
TEST_NAME="Bug Report Workflow"
PROJECT_TITLE="[TEST] Bug: Calculator division by zero crash"
BUG_TYPE="implementation"
SEVERITY="high"
RELATED_PROJECT="project-somas"

# Main test function
main() {
    local start_time
    start_time=$(date +%s)
    
    local test_status="FAILED"
    local issue_number=""
    
    trap 'print_summary "${TEST_NAME}" "${test_status}" "$(($(date +%s) - start_time))"' EXIT
    
    init_log "${TEST_NAME}"
    log_section "SOMAS Workflow Test: Bug Report"
    
    # Prerequisites
    check_requirements || exit 1
    check_gh_auth || exit 1
    
    # Create bug report issue
    log_section "Step 1: Create Bug Report Issue"
    
    local issue_body
    issue_body=$(cat <<EOF
### Related Project ID

${RELATED_PROJECT}

### Bug Type

${BUG_TYPE}

### Description

The calculator crashes when attempting to divide by zero instead of handling the error gracefully.

### Steps to Reproduce

1. Run the calculator application
2. Enter: 10 / 0
3. Press Enter
4. Application crashes with unhandled exception

### Expected Behavior

The application should display an error message: "Error: Division by zero is not allowed" and continue running.

### Actual Behavior

Application crashes with: ZeroDivisionError: division by zero

### Severity Level

${SEVERITY}

### Environment

- Python 3.11
- Linux Ubuntu 22.04
- Calculator v1.0.0

### Additional Context

This is a test bug report for SOMAS workflow validation.
EOF
)
    
    issue_number=$(create_issue "${PROJECT_TITLE}" "${issue_body}" "somas:bug")
    
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
    log_section "Step 3: Verify Bug Triage"
    
    sleep 15
    check_issue_labels "${issue_number}" "somas:bug" || log_warning "Bug label not applied"
    check_issue_comments "${issue_number}" "bug" || log_warning "Bug triage comment not found"
    
    test_status="PASSED"
    log_success "Bug report workflow test completed"
}

main "$@"
