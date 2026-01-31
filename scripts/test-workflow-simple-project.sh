#!/usr/bin/env bash
#
# test-workflow-simple-project.sh
# Test SOMAS workflow with a simple project submission
#
# This script:
# 1. Creates a new GitHub issue using the somas-project template
# 2. Monitors the automated pipeline execution
# 3. Validates each stage and artifact generation
# 4. Verifies PR creation and quality gates
# 5. Logs all steps to log.txt

set -euo pipefail

# Load helper functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/workflow-test-helpers.sh
source "${SCRIPT_DIR}/lib/workflow-test-helpers.sh"

# Configuration
TEST_NAME="Simple Project Workflow"
CLEANUP_ON_SUCCESS=false
CLEANUP_ON_FAILURE=false

# Test parameters
PROJECT_TITLE="[TEST] Simple Calculator Project"
PROJECT_TYPE="new_project"
COMPLEXITY="medium"
PRIORITY="medium"
LANGUAGE="Python"

# Expected labels at each stage
EXPECTED_LABELS_INITIAL=("somas-project")
EXPECTED_LABELS_TRIAGED=("somas-project" "somas:triaged" "somas:dev")

# Expected artifacts
EXPECTED_ARTIFACTS=(
    "project_request.md"
    "initial_plan.yml"
    "SPEC.md"
    "execution_plan.yml"
    "ARCHITECTURE.md"
)

# Main test function
main() {
    local start_time
    start_time=$(date +%s)
    
    # Use global variable for test_status so cleanup_handler can access it
    test_status="FAILED"
    local issue_number=""
    local pr_number=""
    
    # Trap to ensure cleanup
    trap 'cleanup_handler "${issue_number}" "${pr_number}"' EXIT
    
    # Initialize
    init_log "${TEST_NAME}"
    log_section "SOMAS Workflow Test: Simple Project"
    
    # Prerequisites
    log_section "Prerequisites Check"
    if ! check_requirements; then
        log_error "Prerequisites not met"
        exit 1
    fi
    
    if ! check_gh_auth; then
        log_error "GitHub authentication failed"
        exit 1
    fi
    
    local repo_info
    repo_info=$(get_repo_info)
    log_info "Repository: ${repo_info}"
    
    # Step 1: Create Issue
    log_section "Step 1: Create Test Issue"
    
    local issue_body
    issue_body=$(cat <<EOF
### Project Idea

A simple command-line calculator that supports basic arithmetic operations (addition, subtraction, multiplication, division).

### Project Type

${PROJECT_TYPE}

### Complexity Level

${COMPLEXITY}

### Priority Level

${PRIORITY}

### Programming Language Preference

${LANGUAGE}

### Technical Constraints

- Must be command-line interface
- Must support decimal numbers
- Must handle division by zero gracefully
- Must include comprehensive tests

### Additional Context

This is an automated test of the SOMAS workflow pipeline. The project should be simple enough to complete quickly but complex enough to test all stages.
EOF
)
    
    issue_number=$(create_issue "${PROJECT_TITLE}" "${issue_body}" "somas-project")
    
    if [ -z "${issue_number}" ]; then
        log_error "Failed to create issue"
        exit 1
    fi
    
    log_info "Issue URL: https://github.com/${repo_info}/issues/${issue_number}"
    
    # Step 2: Wait for intake/triage workflow
    log_section "Step 2: Monitor Intake/Triage Workflow"
    
    local intake_run_id
    if intake_run_id=$(wait_for_workflow_trigger "intake-triage.yml" "${issue_number}" 60); then
        log_success "Intake workflow triggered"
        
        if monitor_workflow "${intake_run_id}" 30; then
            log_success "Intake workflow completed"
        else
            log_error "Intake workflow failed"
            get_workflow_logs "${intake_run_id}"
            exit 1
        fi
    else
        log_warning "Intake workflow did not trigger (may not exist or may be disabled)"
    fi
    
    # Step 3: Verify labels after triage
    log_section "Step 3: Verify Triage Labels"
    
    sleep 10  # Give time for labels to be applied
    
    if check_issue_labels "${issue_number}" "${EXPECTED_LABELS_TRIAGED[@]}"; then
        log_success "Triage labels verified"
    else
        log_warning "Some triage labels missing (may be added later)"
    fi
    
    # Step 4: Monitor main pipeline
    log_section "Step 4: Monitor Main Pipeline"
    
    local pipeline_run_id
    if pipeline_run_id=$(wait_for_workflow_trigger "somas-pipeline.yml" "${issue_number}" 120); then
        log_success "Main pipeline triggered (Run ID: ${pipeline_run_id})"
        log_info "Pipeline URL: https://github.com/${repo_info}/actions/runs/${pipeline_run_id}"
        
        # Monitor with longer intervals for pipeline (it's a long-running workflow)
        log_info "Monitoring pipeline execution (this may take 15-30 minutes)..."
        
        if monitor_workflow "${pipeline_run_id}" 60; then
            log_success "Main pipeline completed successfully"
        else
            log_error "Main pipeline failed"
            get_workflow_logs "${pipeline_run_id}"
            exit 1
        fi
    else
        log_error "Main pipeline did not trigger"
        exit 1
    fi
    
    # Step 5: Verify project structure
    log_section "Step 5: Verify Project Structure"
    
    local project_id="project-${issue_number}"
    
    if verify_project_structure "${project_id}"; then
        log_success "Project structure verified"
    else
        log_error "Project structure verification failed"
        exit 1
    fi
    
    # Step 6: Verify artifacts (with retries)
    log_section "Step 6: Verify Artifacts"
    
    sleep 30  # Give time for final commits
    
    # Pull latest changes to see artifacts
    log_info "Pulling latest changes..."
    git pull || log_warning "Could not pull latest changes"
    
    local artifacts_found=0
    for artifact in "${EXPECTED_ARTIFACTS[@]}"; do
        if verify_artifacts "${project_id}" "${artifact}"; then
            artifacts_found=$((artifacts_found + 1))
        fi
    done
    
    log_info "Artifacts found: ${artifacts_found}/${#EXPECTED_ARTIFACTS[@]}"
    
    if [ ${artifacts_found} -ge 3 ]; then
        log_success "Core artifacts verified (${artifacts_found} found)"
    else
        log_warning "Some artifacts missing (${artifacts_found} found)"
    fi
    
    # Step 7: Wait for PR creation
    log_section "Step 7: Wait for PR Creation"
    
    if pr_number=$(wait_for_pr "${issue_number}" 300); then
        log_success "PR created successfully"
        log_info "PR URL: https://github.com/${repo_info}/pull/${pr_number}"
        
        verify_pr "${pr_number}"
    else
        log_error "PR was not created"
        log_info "Checking for PR creation comment on issue..."
        check_issue_comments "${issue_number}" "PR Creation Pending" || true
        exit 1
    fi
    
    # Step 8: Verify issue comments
    log_section "Step 8: Verify Issue Comments"
    
    check_issue_comments "${issue_number}" "triage" || log_warning "Triage comment not found"
    check_issue_comments "${issue_number}" "Pipeline Complete" || log_warning "Completion comment not found"
    
    # Success!
    test_status="PASSED"
    
    local end_time
    end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    print_summary "${TEST_NAME}" "${test_status}" "${duration}"
    
    log_success "Test completed successfully!"
    log_info "Issue #${issue_number} can be reviewed and closed manually"
    if [ -n "${pr_number}" ]; then
        log_info "PR #${pr_number} can be reviewed and merged manually"
    fi
}

# Cleanup handler
cleanup_handler() {
    local issue_number="$1"
    local pr_number="$2"
    
    if [ "${test_status}" = "PASSED" ] && [ "${CLEANUP_ON_SUCCESS}" = true ]; then
        cleanup_test "${issue_number}" "${pr_number}"
    elif [ "${test_status}" = "FAILED" ] && [ "${CLEANUP_ON_FAILURE}" = true ]; then
        cleanup_test "${issue_number}" "${pr_number}"
    else
        log_info "Skipping cleanup (resources left for manual review)"
    fi
}

# Run main function
main "$@"
