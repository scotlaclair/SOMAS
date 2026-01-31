#!/usr/bin/env bash
#
# test-workflow-all.sh
# Run all SOMAS workflow tests
#
# This script runs all workflow test scenarios and generates a combined report

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
COMBINED_LOG="${PROJECT_ROOT}/workflow-tests-combined.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test scenarios
declare -a TEST_SCRIPTS=(
    "test-workflow-simple-project.sh"
    "test-workflow-bug-report.sh"
    "test-workflow-enhancement.sh"
)

# Test results
declare -A TEST_RESULTS
declare -A TEST_DURATIONS

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "${COMBINED_LOG}"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "${COMBINED_LOG}"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "${COMBINED_LOG}"
}

log_section() {
    echo "" | tee -a "${COMBINED_LOG}"
    echo "========================================" | tee -a "${COMBINED_LOG}"
    echo "  $1" | tee -a "${COMBINED_LOG}"
    echo "========================================" | tee -a "${COMBINED_LOG}"
}

# Initialize combined log
init_combined_log() {
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    {
        echo "========================================="
        echo "SOMAS Workflow Tests - All Scenarios"
        echo "Started: ${timestamp}"
        echo "========================================="
        echo ""
    } > "${COMBINED_LOG}"
    
    log_info "Combined log file: ${COMBINED_LOG}"
}

# Run a single test
run_test() {
    local test_script="$1"
    local test_name="${test_script%.sh}"
    
    log_section "Running: ${test_script}"
    
    local start_time
    start_time=$(date +%s)
    
    local test_log="${PROJECT_ROOT}/log-${test_name}.txt"
    
    # Set custom log file for this test
    export LOG_FILE="${test_log}"
    
    if bash "${SCRIPT_DIR}/${test_script}"; then
        TEST_RESULTS["${test_script}"]="PASSED"
        log_success "${test_script} - PASSED"
    else
        TEST_RESULTS["${test_script}"]="FAILED"
        log_error "${test_script} - FAILED"
    fi
    
    local end_time
    end_time=$(date +%s)
    local duration=$((end_time - start_time))
    TEST_DURATIONS["${test_script}"]="${duration}"
    
    log_info "Duration: ${duration}s"
    log_info "Individual log: ${test_log}"
    
    # Append individual log to combined log
    {
        echo ""
        echo "--- ${test_script} Log ---"
        cat "${test_log}" || echo "Could not read log file"
        echo "--- End ${test_script} Log ---"
        echo ""
    } >> "${COMBINED_LOG}"
}

# Print final summary
print_final_summary() {
    log_section "Final Summary"
    
    local total_tests=${#TEST_SCRIPTS[@]}
    local passed_tests=0
    local failed_tests=0
    local total_duration=0
    
    for test_script in "${TEST_SCRIPTS[@]}"; do
        local result="${TEST_RESULTS[${test_script}]:-UNKNOWN}"
        local duration="${TEST_DURATIONS[${test_script}]:-0}"
        
        total_duration=$((total_duration + duration))
        
        if [ "${result}" = "PASSED" ]; then
            passed_tests=$((passed_tests + 1))
            log_success "✓ ${test_script} - ${duration}s"
        else
            failed_tests=$((failed_tests + 1))
            log_error "✗ ${test_script} - ${duration}s"
        fi
    done
    
    log_info ""
    log_info "Total Tests: ${total_tests}"
    log_info "Passed: ${passed_tests}"
    log_info "Failed: ${failed_tests}"
    log_info "Total Duration: ${total_duration}s"
    
    if [ ${failed_tests} -eq 0 ]; then
        log_success "All tests passed!"
        return 0
    else
        log_error "Some tests failed"
        return 1
    fi
}

# Main function
main() {
    local start_time
    start_time=$(date +%s)
    
    log_section "SOMAS Workflow Test Suite"
    
    init_combined_log
    
    log_info "Running ${#TEST_SCRIPTS[@]} test scenarios..."
    log_info ""
    
    # Check if test scripts exist
    for test_script in "${TEST_SCRIPTS[@]}"; do
        if [ ! -f "${SCRIPT_DIR}/${test_script}" ]; then
            log_error "Test script not found: ${test_script}"
            exit 1
        fi
        
        if [ ! -x "${SCRIPT_DIR}/${test_script}" ]; then
            log_info "Making ${test_script} executable..."
            chmod +x "${SCRIPT_DIR}/${test_script}"
        fi
    done
    
    # Run all tests
    for test_script in "${TEST_SCRIPTS[@]}"; do
        run_test "${test_script}"
        
        # Brief pause between tests
        sleep 5
    done
    
    # Print summary
    local summary_result=0
    print_final_summary || summary_result=$?
    
    local end_time
    end_time=$(date +%s)
    local total_duration=$((end_time - start_time))
    
    log_info ""
    log_info "Test suite completed in ${total_duration}s"
    log_info "Combined log: ${COMBINED_LOG}"
    
    # Exit with appropriate code based on summary result
    exit $summary_result
}

# Run main
main "$@"
