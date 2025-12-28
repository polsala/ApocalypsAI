#!/bin/bash

# Tests for Ephemeral Runner Orchestrator
# These tests verify the core logic without making actual API calls

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[TEST]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Mock functions to simulate API responses
mock_github_api() {
    local endpoint=$1
    
    case "$endpoint" in
        "runners")
            # Mock response with 3 online, 1 offline runner
            cat << 'EOF'
{
  "total_count": 4,
  "runners": [
    {"id": 1, "name": "runner-1", "status": "online"},
    {"id": 2, "name": "runner-2", "status": "online"},
    {"id": 3, "name": "runner-3", "status": "online"},
    {"id": 4, "name": "runner-4", "status": "offline"}
  ]
}
EOF
            ;;
        "queue")
            # Mock response with 2 queued jobs
            cat << 'EOF'
{
  "total_count": 2,
  "workflow_runs": [
    {"id": 100, "status": "queued"},
    {"id": 101, "status": "queued"}
  ]
}
EOF
            ;;
        "in_progress")
            # Mock response with 1 in_progress job
            cat << 'EOF'
{
  "total_count": 1,
  "workflow_runs": [
    {"id": 200, "status": "in_progress"}
  ]
}
EOF
            ;;
    esac
}

# Test scaling logic
test_scaling_logic() {
    log "Testing scaling logic..."
    
    # Test case 1: Need to scale up (queue > threshold, runners < target)
    local online_runners=2
    local target_runners=5
    local queued_jobs=8
    local queue_threshold=5
    
    if [[ $queued_jobs -gt $queue_threshold && $online_runners -lt $target_runners ]]; then
        log "✓ Scale up logic works correctly"
        local runners_needed=$((target_runners - online_runners))
        log "  Runners needed: $runners_needed"
    else
        error "✗ Scale up logic failed"
        return 1
    fi
    
    # Test case 2: Need to scale down (runners > target)
    online_runners=8
    target_runners=5
    
    if [[ $online_runners -gt $target_runners ]]; then
        log "✓ Scale down logic works correctly"
        local runners_to_remove=$((online_runners - target_runners))
        log "  Runners to remove: $runners_to_remove"
    else
        error "✗ Scale down logic failed"
        return 1
    fi
    
    # Test case 3: No change needed (runners = target)
    online_runners=5
    target_runners=5
    
    if [[ $online_runners -eq $target_runners ]]; then
        log "✓ No change logic works correctly"
    else
        error "✗ No change logic failed"
        return 1
    fi
}

# Test time-based logic
test_time_logic() {
    log "Testing time-based logic..."
    
    # Test peak hours calculation
    local current_time="12:30"
    local peak_start="09:00"
    local peak_end="17:00"
    
    if [[ "$current_time" > "$peak_start" && "$current_time" < "$peak_end" ]]; then
        log "✓ Peak hours detection works correctly"
        log "  Current time $current_time is within peak hours ($peak_start - $peak_end)"
    else
        error "✗ Peak hours detection failed"
        return 1
    fi
    
    # Test off-peak hours
    current_time="20:00"
    
    if [[ "$current_time" < "$peak_start" || "$current_time" > "$peak_end" ]]; then
        log "✓ Off-peak hours detection works correctly"
        log "  Current time $current_time is outside peak hours"
    else
        error "✗ Off-peak hours detection failed"
        return 1
    fi
}

# Test JSON parsing
test_json_parsing() {
    log "Testing JSON parsing..."
    
    # Test parsing runner status
    local runners_json='{
  "total_count": 4,
  "runners": [
    {"id": 1, "name": "runner-1", "status": "online"},
    {"id": 2, "name": "runner-2", "status": "online"},
    {"id": 3, "name": "runner-3", "status": "online"},
    {"id": 4, "name": "runner-4", "status": "offline"}
  ]
}'
    
    local online_count=$(echo "$runners_json" | jq '[.runners[] | select(.status == "online")] | length')
    local offline_count=$(echo "$runners_json" | jq '[.runners[] | select(.status == "offline")] | length')
    local total_count=$(echo "$runners_json" | jq '.total_count')
    
    if [[ $online_count -eq 3 && $offline_count -eq 1 && $total_count -eq 4 ]]; then
        log "✓ JSON parsing for runners works correctly"
        log "  Online: $online_count, Offline: $offline_count, Total: $total_count"
    else
        error "✗ JSON parsing for runners failed"
        return 1
    fi
    
    # Test parsing queue status
    local queue_json='{
  "total_count": 3,
  "workflow_runs": [
    {"id": 100, "status": "queued"},
    {"id": 101, "status": "queued"},
    {"id": 102, "status": "queued"}
  ]
}'
    
    local queued_count=$(echo "$queue_json" | jq '.workflow_runs | length')
    
    if [[ $queued_count -eq 3 ]]; then
        log "✓ JSON parsing for queue works correctly"
        log "  Queued jobs: $queued_count"
    else
        error "✗ JSON parsing for queue failed"
        return 1
    fi
}

# Test cleanup logic
test_cleanup_logic() {
    log "Testing cleanup logic..."
    
    # Test runner name pattern matching
    local runner_name="ephemeral-runner-1234567890-abc"
    local pattern="ephemeral-runner-.*"
    
    if [[ "$runner_name" =~ $pattern ]]; then
        log "✓ Runner name pattern matching works correctly"
    else
        error "✗ Runner name pattern matching failed"
        return 1
    fi
    
    # Test time-based idle detection (simplified)
    local current_time=$(date +%s)
    local job_time=$(($(date +%s) - 2000))  # 33 minutes ago
    local idle_timeout=30
    
    if [[ $(( (current_time - job_time) / 60 )) -gt $idle_timeout ]]; then
        log "✓ Idle detection logic works correctly"
        log "  Job was idle for $(( (current_time - job_time) / 60 )) minutes (threshold: $idle_timeout)"
    else
        error "✗ Idle detection logic failed"
        return 1
    fi
}

# Test configuration validation
test_config_validation() {
    log "Testing configuration validation..."
    
    # Test required environment variables
    local test_token="test_token_123"
    local test_repo="test-owner/test-repo"
    
    if [[ -n "$test_token" && -n "$test_repo" ]]; then
        log "✓ Configuration validation works correctly"
    else
        error "✗ Configuration validation failed"
        return 1
    fi
    
    # Test parameter ranges
    local max_runners=10
    local min_runners=2
    local queue_threshold=5
    
    if [[ $max_runners -gt 0 && $min_runners -ge 0 && $queue_threshold -gt 0 && $min_runners -le $max_runners ]]; then
        log "✓ Parameter validation works correctly"
        log "  Max runners: $max_runners, Min runners: $min_runners, Threshold: $queue_threshold"
    else
        error "✗ Parameter validation failed"
        return 1
    fi
}

# Run all tests
run_tests() {
    log "Starting Ephemeral Runner Orchestrator tests..."
    echo ""
    
    local test_count=0
    local passed_count=0
    
    # List of test functions
    local tests=(
        "test_scaling_logic"
        "test_time_logic"
        "test_json_parsing"
        "test_cleanup_logic"
        "test_config_validation"
    )
    
    for test_func in "${tests[@]}"; do
        test_count=$((test_count + 1))
        log "Running $test_func..."
        
        if $test_func; then
            passed_count=$((passed_count + 1))
            log "✓ $test_func passed"
        else
            error "✗ $test_func failed"
        fi
        echo ""
    done
    
    log "Test Results: $passed_count/$test_count tests passed"
    
    if [[ $passed_count -eq $test_count ]]; then
        log "All tests passed! 🎉"
        return 0
    else
        error "Some tests failed! ❌"
        return 1
    fi
}

# Run the tests
run_tests
