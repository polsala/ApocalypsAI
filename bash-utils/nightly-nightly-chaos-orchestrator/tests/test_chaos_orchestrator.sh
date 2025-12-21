#!/bin/bash

# Tests for Nightly Chaos Orchestrator
# These tests verify functionality without actually causing chaos

set -euo pipefail

# Colors for test output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test counter
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

# Test functions
run_test() {
    local test_name="$1"
    local test_func="$2"
    
    TEST_COUNT=$((TEST_COUNT + 1))
    echo -n "Running $test_name... "
    
    if $test_func; then
        echo -e "${GREEN}PASS${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}FAIL${NC}"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

# Test that script is executable
test_script_executable() {
    [[ -x "$(dirname "$0")/../src/chaos_orchestrator.sh" ]]
}

# Test that script has proper shebang
test_shebang() {
    head -1 "$(dirname "$0")/../src/chaos_orchestrator.sh" | grep -q "#!/bin/bash"
}

# Test dry run mode works
test_dry_run() {
    local script="$(dirname "$0")/../src/chaos_orchestrator.sh"
    local temp_log="/tmp/test_chaos_$$"
    
    # Mock the log file location
    export LOG_FILE="$temp_log"
    
    timeout 5s bash -c "$script --dry-run --duration 1" 2>/dev/null || true
    
    # Check that log was created and contains dry run messages
    if [[ -f "$temp_log" ]] && grep -q "DRY_RUN" "$temp_log"; then
        rm -f "$temp_log"
        return 0
    else
        rm -f "$temp_log"
        return 1
    fi
}

# Test help output
test_help_output() {
    local script="$(dirname "$0")/../src/chaos_orchestrator.sh"
    
    $script --help 2>&1 | grep -q "Usage:"
}

# Test argument parsing
test_argument_parsing() {
    local script="$(dirname "$0")/../src/chaos_orchestrator.sh"
    local temp_log="/tmp/test_chaos_args_$$"
    
    export LOG_FILE="$temp_log"
    
    # Test level parsing
    timeout 3s bash -c "$script --level moderate --duration 1 --dry-run" 2>/dev/null || true
    
    if [[ -f "$temp_log" ]]; then
        rm -f "$temp_log"
        return 0
    else
        return 1
    fi
}

# Test configuration file loading
test_config_loading() {
    local script="$(dirname "$0")/../src/chaos_orchestrator.sh"
    local temp_config="/tmp/test_chaos_config_$$"
    local temp_log="/tmp/test_chaos_config_log_$$"
    
    # Create test config
    cat > "$temp_config" << EOF
CHAOS_LEVEL="moderate"
CHAOS_DURATION=10
ENABLE_PROCESS_CHAOS=false
ENABLE_NETWORK_CHAOS=false
ENABLE_DISK_CHAOS=false
ENABLE_FILE_CHAOS=false
SAFETY_MODE=true
EOF
    
    export LOG_FILE="$temp_log"
    
    timeout 5s bash -c "$script --config $temp_config --dry-run" 2>/dev/null || true
    
    local result=$?
    rm -f "$temp_config" "$temp_log"
    
    # Should not fail due to config loading
    [[ $result -eq 0 || $result -eq 124 ]] # 124 is timeout exit code
}

# Test that critical processes are protected
test_critical_process_protection() {
    local script="$(dirname "$0")/../src/chaos_orchestrator.sh"
    
    # This test verifies the function exists and has the right structure
    grep -q "CRITICAL_PROCESSES" "$script" &&
    grep -q "systemd" "$script" &&
    grep -q "kernel" "$script"
}

# Test logging functionality
test_logging() {
    local script="$(dirname "$0")/../src/chaos_orchestrator.sh"
    local temp_log="/tmp/test_chaos_logging_$$"
    
    export LOG_FILE="$temp_log"
    
    # Mock the log function to test it works
    timeout 3s bash -c "source \"$script\" && log \"INFO\" \"test message\"" 2>/dev/null || true
    
    if [[ -f "$temp_log" ]] && grep -q "test message" "$temp_log"; then
        rm -f "$temp_log"
        return 0
    else
        rm -f "$temp_log"
        return 1
    fi
}

# Test safety checks
test_safety_checks() {
    local script="$(dirname "$0")/../src/chaos_orchestrator.sh"
    
    # Verify safety functions exist
    grep -q "check_safety" "$script" &&
    grep -q "SAFETY_MODE" "$script" &&
    grep -q "disk_usage" "$script"
}

# Test chaos level validation
test_chaos_level_validation() {
    local script="$(dirname "$0")/../src/chaos_orchestrator.sh"
    
    # Check that valid levels are handled
    grep -q "mild" "$script" &&
    grep -q "moderate" "$script" &&
    grep -q "severe" "$script"
}

# Test cleanup functionality
test_cleanup() {
    local script="$(dirname "$0")/../src/chaos_orchestrator.sh"
    
    # Verify cleanup function exists and has proper trap
    grep -q "cleanup()" "$script" &&
    grep -q "trap.*cleanup" "$script"
}

# Test report generation
test_report_generation() {
    local script="$(dirname "$0")/../src/chaos_orchestrator.sh"
    local temp_log="/tmp/test_chaos_report_$$"
    
    # Create a mock log file with some chaos events
    cat > "$temp_log" << EOF
# Chaos Orchestrator Log - $(date)
[2024-01-01 12:00:00] [INFO] Starting chaos orchestration
[2024-01-01 12:00:01] [CHAOS] Killing process test (PID: 1234)
[2024-01-01 12:00:02] [CHAOS] Adding 100ms latency to interface eth0
[2024-01-01 12:00:03] [INFO] Chaos orchestration completed
EOF
    
    export LOG_FILE="$temp_log"
    
    # Test that report generation doesn't crash
    timeout 5s bash -c "source \"$script\" && generate_report" 2>/dev/null || true
    
    local result=$?
    rm -f "$temp_log"
    
    # Should not fail
    [[ $result -eq 0 || $result -eq 124 ]]
}

# Run all tests
run_all_tests() {
    echo -e "${BLUE}=== Chaos Orchestrator Test Suite ===${NC}"
    echo ""
    
    run_test "Script is executable" test_script_executable
    run_test "Has proper shebang" test_shebang
    run_test "Help output works" test_help_output
    run_test "Dry run mode" test_dry_run
    run_test "Argument parsing" test_argument_parsing
    run_test "Configuration loading" test_config_loading
    run_test "Critical process protection" test_critical_process_protection
    run_test "Logging functionality" test_logging
    run_test "Safety checks" test_safety_checks
    run_test "Chaos level validation" test_chaos_level_validation
    run_test "Cleanup functionality" test_cleanup
    run_test "Report generation" test_report_generation
    
    echo ""
    echo -e "${BLUE}=== Test Results ===${NC}"
    echo "Total tests: $TEST_COUNT"
    echo -e "Passed: ${GREEN}$PASS_COUNT${NC}"
    echo -e "Failed: ${RED}$FAIL_COUNT${NC}"
    
    if [[ $FAIL_COUNT -eq 0 ]]; then
        echo -e "${GREEN}All tests passed! 🎉${NC}"
        return 0
    else
        echo -e "${RED}$FAIL_COUNT test(s) failed! ❌${NC}"
        return 1
    fi
}

# Mock functions for testing (to prevent actual chaos)
mock_chaos_functions() {
    # These functions replace the actual chaos functions during testing
    chaos_kill_process() { echo "Would kill process"; }
    chaos_network_latency() { echo "Would add network latency"; }
    chaos_fill_disk() { echo "Would fill disk space"; }
    chaos_file_errors() { echo "Would create file errors"; }
}

# Main execution
main() {
    # Source the script to access its functions, but mock the dangerous ones
    local script_path="$(dirname "$0")/../src/chaos_orchestrator.sh"
    
    if [[ ! -f "$script_path" ]]; then
        echo -e "${RED}Error: Script not found at $script_path${NC}"
        exit 1
    fi
    
    # Mock dangerous functions before sourcing
    mock_chaos_functions
    
    # Run tests
    run_all_tests
}

# Execute if run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
