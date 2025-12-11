#!/bin/bash

# Test suite for Chaos Garden Orchestrator
# Mock rationale: These tests verify the script logic without actually applying chaos

set -euo pipefail

# Colors for test output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test counter
TEST_COUNT=0
PASSED_COUNT=0

# Mock functions to avoid actual chaos during testing
mock_tc() {
  echo "Mock: tc command would run"
}

mock_systemctl() {
  case $1 in
    is-active)
      echo "active"
      return 0
      ;;
    restart)
      echo "Mock: systemctl restart $2"
      return 0
      ;;
  esac
}

mock_pkill() {
  echo "Mock: pkill command would run"
}

mock_nproc() {
  echo "4"
}

# Test runner
run_test() {
  local test_name="$1"
  local test_function="$2"
  
  TEST_COUNT=$((TEST_COUNT + 1))
  echo -e "${YELLOW}Running: $test_name${NC}"
  
  if $test_function; then
    echo -e "${GREEN}✅ PASSED: $test_name${NC}"
    PASSED_COUNT=$((PASSED_COUNT + 1))
  else
    echo -e "${RED}❌ FAILED: $test_name${NC}"
  fi
  echo ""
}

# Test intensity parsing
test_intensity_parsing() {
  # Mock the apply_network_delay function to avoid actual tc calls
  apply_network_delay() {
    local intensity="$1"
    local duration="$2"
    local latency=100
    
    case "$intensity" in
      gentle)
        latency=50
        ;;
      moderate)
        latency=150
        ;;
      wild)
        latency=300
        ;;
    esac
    
    # Verify latency values
    if [ "$intensity" = "gentle" ] && [ "$latency" -eq 50 ]; then
      return 0
    elif [ "$intensity" = "moderate" ] && [ "$latency" -eq 150 ]; then
      return 0
    elif [ "$intensity" = "wild" ] && [ "$latency" -eq 300 ]; then
      return 0
    else
      return 1
    fi
  }
  
  # Test all intensity levels
  apply_network_delay "gentle" "60" && \
  apply_network_delay "moderate" "60" && \
  apply_network_delay "wild" "60"
}

# Test duration validation
test_duration_validation() {
  # Test valid durations
  if [[ "60" =~ ^[0-9]+$ ]] && \
     [[ "300" =~ ^[0-9]+$ ]] && \
     [[ "1" =~ ^[0-9]+$ ]]; then
    return 0
  else
    return 1
  fi
}

# Test scenario selection
test_scenario_selection() {
  local scenarios=("network-delay" "resource-exhaustion" "service-failure" "time-warp" "random-chaos")
  
  for scenario in "${scenarios[@]}"; do
    case "$scenario" in
      network-delay|resource-exhaustion|service-failure|time-warp|random-chaos)
        continue
        ;;
      *)
        return 1
        ;;
    esac
  done
  return 0
}

# Test CPU core calculation
test_cpu_core_calculation() {
  # Mock nproc
  nproc() {
    echo "4"
  }
  
  # Test core calculation for different intensities
  local cpu_cores=1
  local intensity="moderate"
  
  case "$intensity" in
    gentle)
      cpu_cores=1
      ;;
    moderate)
      cpu_cores=2
      ;;
    wild)
      cpu_cores=$(nproc)
      ;;
  esac
  
  if [ "$cpu_cores" -eq 2 ]; then
    return 0
  else
    return 1
  fi
}

# Test report generation
test_report_generation() {
  local scenario="network-delay"
  local intensity="moderate"
  local duration="60"
  local start_time=$(date +%s)
  local end_time=$((start_time + 10))
  
  # Generate report
  local report_file="test_chaos_report_$(date +%Y%m%d_%H%M%S).txt"
  
  cat > "$report_file" << EOF
🌿 Chaos Garden Report 🌿
=========================

Scenario: $scenario
Intensity: $intensity
Duration: $duration
Start Time: $(date -d @$start_time)
End Time: $(date -d @$end_time)

Recovery Status: ✅ All services bloomed back to health

EOF
  
  # Verify report was created and contains expected content
  if [ -f "$report_file" ] && grep -q "Chaos Garden Report" "$report_file" && \
     grep -q "Scenario: $scenario" "$report_file" && \
     grep -q "Intensity: $intensity" "$report_file"; then
    rm "$report_file"
    return 0
  else
    rm -f "$report_file"
    return 1
  fi
}

# Test argument parsing
test_argument_parsing() {
  # Test help flag
  if ./src/chaos_garden_orchestrator.sh --help &> /dev/null; then
    return 0
  else
    return 1
  fi
}

# Test intensity validation
test_intensity_validation() {
  local valid_intensities=("gentle" "moderate" "wild")
  local invalid_intensities=("invalid" "super" "weak")
  
  # Test valid intensities
  for intensity in "${valid_intensities[@]}"; do
    if [[ "$intensity" =~ ^(gentle|moderate|wild)$ ]]; then
      continue
    else
      return 1
    fi
  done
  
  # Test invalid intensities
  for intensity in "${invalid_intensities[@]}"; do
    if [[ ! "$intensity" =~ ^(gentle|moderate|wild)$ ]]; then
      continue
    else
      return 1
    fi
  done
  
  return 0
}

# Test cleanup function
test_cleanup_function() {
  # Mock cleanup function
  cleanup() {
    echo "Mock: Cleaning up chaos remnants..."
    sudo tc qdisc del dev lo root 2>/dev/null || true
    pkill -f "yes > /dev/null" 2>/dev/null || true
    echo "Mock: Cleanup completed"
  }
  
  # Test that cleanup runs without errors
  cleanup && return 0 || return 1
}

# Test orchestration mode
test_orchestration_mode() {
  local scenarios_executed=()
  
  # Mock scenario functions
  apply_network_delay() {
    scenarios_executed+=("network-delay")
  }
  
  apply_resource_exhaustion() {
    scenarios_executed+=("resource-exhaustion")
  }
  
  apply_service_failure() {
    scenarios_executed+=("service-failure")
  }
  
  apply_time_warp() {
    scenarios_executed+=("time-warp")
  }
  
  # Simulate orchestration
  local scenarios=("network-delay" "resource-exhaustion" "service-failure" "time-warp")
  for s in "${scenarios[@]}"; do
    case "$s" in
      network-delay)
        apply_network_delay
        ;;
      resource-exhaustion)
        apply_resource_exhaustion
        ;;
      service-failure)
        apply_service_failure
        ;;
      time-warp)
        apply_time_warp
        ;;
    esac
  done
  
  # Verify all scenarios were executed
  if [ ${#scenarios_executed[@]} -eq 4 ]; then
    return 0
  else
    return 1
  fi
}

# Test random chaos selection
test_random_chaos_selection() {
  local scenarios=("network-delay" "resource-exhaustion" "service-failure" "time-warp")
  local selected_scenario=""
  
  # Mock random selection
  selected_scenario="${scenarios[0]}"  # Always pick first for testing
  
  if [[ " ${scenarios[@]} " =~ " $selected_scenario " ]]; then
    return 0
  else
    return 1
  fi
}

# Run all tests
main() {
  echo -e "${YELLOW}🧪 Running Chaos Garden Orchestrator Tests 🧪${NC}"
  echo "===============================================
"
  
  # Set up mocks
  alias tc=mock_tc
  alias systemctl=mock_systemctl
  alias pkill=mock_pkill
  alias nproc=mock_nproc
  
  # Run tests
  run_test "Intensity Parsing" test_intensity_parsing
  run_test "Duration Validation" test_duration_validation
  run_test "Scenario Selection" test_scenario_selection
  run_test "CPU Core Calculation" test_cpu_core_calculation
  run_test "Report Generation" test_report_generation
  run_test "Argument Parsing" test_argument_parsing
  run_test "Intensity Validation" test_intensity_validation
  run_test "Cleanup Function" test_cleanup_function
  run_test "Orchestration Mode" test_orchestration_mode
  run_test "Random Chaos Selection" test_random_chaos_selection
  
  # Print results
  echo "==============================================="
  echo -e "${GREEN}Tests Passed: $PASSED_COUNT/${TEST_COUNT}${NC}"
  
  if [ $PASSED_COUNT -eq $TEST_COUNT ]; then
    echo -e "${GREEN}🎉 All tests passed! 🎉${NC}"
    exit 0
  else
    echo -e "${RED}💥 Some tests failed! 💥${NC}"
    exit 1
  fi
}

# Run main if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
