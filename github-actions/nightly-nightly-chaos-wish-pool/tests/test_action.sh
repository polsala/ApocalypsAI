#!/bin/bash
set -euo pipefail

echo "🧪 Testing Chaos Wish Pool Action"

test_missing_scenarios() {
  echo "Test: Missing scenario file"
  if ./action.yml --scenario-file "nonexistent.yml"; then
    echo "❌ Should have failed with missing file"
    exit 1
  fi
  echo "✅ Correctly failed with missing scenario file"
}

test_missing_approval() {
  echo "Test: Missing CHAOS_APPROVED environment variable"
  if CHAOS_APPROVED="" ./action.yml; then
    echo "❌ Should have failed without approval"
    exit 1
  fi
  echo "✅ Correctly failed without CHAOS_APPROVED"
}

test_invalid_approval() {
  echo "Test: Invalid CHAOS_APPROVED value"
  if CHAOS_APPROVED="false" ./action.yml --scenario-file "tests/test_scenarios.yml"; then
    echo "❌ Should have failed with invalid approval"
    exit 1
  fi
  echo "✅ Correctly failed with invalid CHAOS_APPROVED"
}

test_valid_approval() {
  echo "Test: Valid CHAOS_APPROVED value"
  if CHAOS_APPROVED="true" ./action.yml --scenario-file "tests/test_scenarios.yml"; then
    echo "✅ Action can run with valid approval"
  else
    echo "❌ Action failed with valid approval"
    exit 1
  fi
}

test_scenario_parsing() {
  echo "Test: Scenario parsing"
  SCENARIO="- name: 'Test Scenario'
    description: 'Test description'
    type: branch-rename
    params:
      new_name: 'test-main'
      duration: 300"
  
  # Extract name
  NAME=$(echo "$SCENARIO" | grep -o "name: [^"]*" | cut -d' ' -f2)
  if [ "$NAME" != "Test Scenario" ]; then
    echo "❌ Failed to parse scenario name"
    exit 1
  fi
  
  # Extract type
  TYPE=$(echo "$SCENARIO" | grep -o "type: [^"]*" | cut -d' ' -f2)
  if [ "$TYPE" != "branch-rename" ]; then
    echo "❌ Failed to parse scenario type"
    exit 1
  fi
  
  echo "✅ Scenario parsing works correctly"
}

test_chaos_execution() {
  echo "Test: Chaos scenario execution (mock)"
  SCENARIO="- name: 'Test Scenario'
    type: branch-rename
    params:
      new_name: 'test-main'
      duration: 300"
  
  if ./src/execute_chaos.sh "$SCENARIO" 300 "fake_token"; then
    echo "✅ Chaos execution completed"
  else
    echo "❌ Chaos execution failed"
    exit 1
  fi
}

test_invalid_scenario_type() {
  echo "Test: Invalid scenario type handling"
  SCENARIO="- name: 'Invalid Scenario'
    type: invalid-type"
  
  if ./src/execute_chaos.sh "$SCENARIO" 300 "fake_token"; then
    echo "❌ Should have failed with invalid type"
    exit 1
  fi
  echo "✅ Correctly rejected invalid scenario type"
}

# Run all tests
test_missing_scenarios
test_missing_approval
test_invalid_approval
test_valid_approval
test_scenario_parsing
test_chaos_execution
test_invalid_scenario_type

echo "🎉 All tests passed!"

echo "## 🧪 Chaos Wish Pool Test Results"
echo "All safety checks passed."
echo "The action will only run with explicit approval."
echo "Scenario parsing works correctly."
echo "Invalid inputs are properly rejected."

exit 0
