#!/bin/bash

# Mock rationale: We need to simulate the GitHub Actions environment variables
# and the GITHUB_EVENT_PATH file content to test the script's logic deterministically
# without making actual API calls or relying on a live GitHub event.

set -euo pipefail

# Define the path to the script under test
SCRIPT_PATH="$(dirname "$0")"/../src/check_vibe.sh

# Create temporary files for GITHUB_EVENT_PATH and GITHUB_OUTPUT
GITHUB_EVENT_FILE=$(mktemp)
GITHUB_OUTPUT_FILE=$(mktemp)

# Cleanup function to remove temporary files
cleanup() {
  rm -f "$GITHUB_EVENT_FILE" "$GITHUB_OUTPUT_FILE"
}
trap cleanup EXIT

# Export GITHUB_EVENT_PATH and GITHUB_OUTPUT for the script
export GITHUB_EVENT_PATH="$GITHUB_EVENT_FILE"
export GITHUB_OUTPUT="$GITHUB_OUTPUT_FILE"

# Mock jq for testing purposes if not installed
if ! command -v jq &> /dev/null; then
  echo "Mocking jq for tests..."
  jq() {
    if [ "$1" = "-n" ]; then
      # Simulate jq -n --arg title "$pr_title" '{pull_request: {title: $title}}'
      shift 2 # Remove -n and --arg
      local arg_name="$1"
      local arg_value="$2"
      shift 2 # Remove arg_name and arg_value
      local json_template="$1"
      # Simple replacement for this specific test case
      echo "$json_template" | sed "s/\$$arg_name/\"$arg_value\"/g"
    else
      # Simulate jq -r .pull_request.title "$GITHUB_EVENT_PATH"
      grep -oP '"title":\s*"\K[^"]+' "$GITHUB_EVENT_PATH"
    fi
  }
  export -f jq
fi

# Helper function to run the script with specific inputs and PR title
run_test() {
  local pr_title="$1"
  local required_keywords="$2"
  local forbidden_keywords="$3"
  local fail_on_no_match_required="$4"
  local fail_on_match_forbidden="$5"

  # Write mock PR event to GITHUB_EVENT_FILE
  echo "{\"pull_request\": {\"title\": \"$pr_title\"}}" > "$GITHUB_EVENT_FILE"

  # Set mock input environment variables
  export INPUT_REQUIRED_KEYWORDS="$required_keywords"
  export INPUT_FORBIDDEN_KEYWORDS="$forbidden_keywords"
  export INPUT_FAIL_ON_NO_MATCH_REQUIRED="$fail_on_no_match_required"
  export INPUT_FAIL_ON_MATCH_FORBIDDEN="$fail_on_match_forbidden"

  # Clear previous output
  > "$GITHUB_OUTPUT_FILE"

  # Run the script and capture exit code
  if ! bash "$SCRIPT_PATH"; then
    return 1 # Script failed
  else
    return 0 # Script passed
  fi
}

# Test Cases

# Test 1: PR title with required keyword, no forbidden (PASS)
if run_test "Temporal Anomaly Detected" "temporal" "fix" "true" "true"; then
  if grep -q "vibe-status=pass" "$GITHUB_OUTPUT_FILE"; then
    echo "Test 1 Passed: Required keyword found, no forbidden."
  else
    echo "Test 1 Failed: Expected pass status." && exit 1
  fi
else
  echo "Test 1 Failed: Script exited with error." && exit 1
fi

# Test 2: PR title without required keyword (FAIL due to fail_on_no_match_required=true)
if ! run_test "Add new feature" "temporal" "fix" "true" "true"; then
  if grep -q "vibe-status=fail" "$GITHUB_OUTPUT_FILE"; then
    echo "Test 2 Passed: No required keyword, failed as expected."
  else
    echo "Test 2 Failed: Expected fail status." && exit 1
  fi
else
  echo "Test 2 Failed: Script passed unexpectedly." && exit 1
fi

# Test 3: PR title with forbidden keyword (FAIL due to fail_on_match_forbidden=true)
if ! run_test "Fix bug in void tracker" "temporal" "fix" "true" "true"; then
  if grep -q "vibe-status=fail" "$GITHUB_OUTPUT_FILE"; then
    echo "Test 3 Passed: Forbidden keyword found, failed as expected."
  else
    echo "Test 3 Failed: Expected fail status." && exit 1
  fi
else
  echo "Test 3 Failed: Script passed unexpectedly." && exit 1
fi

# Test 4: PR title with required, but also forbidden (FAIL due to forbidden)
if ! run_test "Fix temporal distortion" "temporal" "fix" "true" "true"; then
  if grep -q "vibe-status=fail" "$GITHUB_OUTPUT_FILE"; then
    echo "Test 4 Passed: Required and forbidden, failed on forbidden as expected."
  else
    echo "Test 4 Failed: Expected fail status." && exit 1
  fi
else
  echo "Test 4 Failed: Script passed unexpectedly." && exit 1
fi

# Test 5: No required keywords, but fail_on_no_match_required=false (PASS)
if run_test "Just a simple update" "temporal" "" "false" "true"; then
  if grep -q "vibe-status=pass" "$GITHUB_OUTPUT_FILE"; then
    echo "Test 5 Passed: No required, but not failing on it."
  else
    echo "Test 5 Failed: Expected pass status." && exit 1
  fi
else
  echo "Test 5 Failed: Script exited with error." && exit 1
fi

# Test 6: Forbidden keyword, but fail_on_match_forbidden=false (PASS)
if run_test "Fix minor issue" "" "fix" "true" "false"; then
  if grep -q "vibe-status=pass" "$GITHUB_OUTPUT_FILE"; then
    echo "Test 6 Passed: Forbidden found, but not failing on it."
  else
    echo "Test 6 Failed: Expected pass status." && exit 1
  fi
else
  echo "Test 6 Failed: Script exited with error." && exit 1
fi

# Test 7: Case insensitivity for required keywords
if run_test "temporal anomaly" "TEMPORAL" "" "true" "true"; then
  if grep -q "vibe-status=pass" "$GITHUB_OUTPUT_FILE"; then
    echo "Test 7 Passed: Case-insensitive required keyword."
  else
    echo "Test 7 Failed: Expected pass status for case-insensitive required." && exit 1
  fi
else
  echo "Test 7 Failed: Script exited with error." && exit 1
fi

# Test 8: Case insensitivity for forbidden keywords
if ! run_test "Fix temporal anomaly" "temporal" "FIX" "true" "true"; then
  if grep -q "vibe-status=fail" "$GITHUB_OUTPUT_FILE"; then
    echo "Test 8 Passed: Case-insensitive forbidden keyword."
  else
    echo "Test 8 Failed: Expected fail status for case-insensitive forbidden." && exit 1
  fi
else
  echo "Test 8 Failed: Script passed unexpectedly." && exit 1
fi

# Test 9: Empty required and forbidden lists (PASS)
if run_test "Any title is fine" "" "" "true" "true"; then
  if grep -q "vibe-status=pass" "$GITHUB_OUTPUT_FILE"; then
    echo "Test 9 Passed: Empty keyword lists."
  else
    echo "Test 9 Failed: Expected pass status for empty lists." && exit 1
  fi
else
  echo "Test 9 Failed: Script exited with error." && exit 1
fi

# Test 10: Multiple required keywords, one found (PASS)
if run_test "Wasteland Scavenger Report" "temporal,wasteland" "" "true" "true"; then
  if grep -q "vibe-status=pass" "$GITHUB_OUTPUT_FILE"; then
    echo "Test 10 Passed: Multiple required, one found."
  else
    echo "Test 10 Failed: Expected pass status for multiple required." && exit 1
  fi
else
  echo "Test 10 Failed: Script exited with error." && exit 1
fi

# Test 11: Multiple forbidden keywords, one found (FAIL)
if ! run_test "Fix the void" "void" "fix,chore" "true" "true"; then
  if grep -q "vibe-status=fail" "$GITHUB_OUTPUT_FILE"; then
    echo "Test 11 Passed: Multiple forbidden, one found."
  else
    echo "Test 11 Failed: Expected fail status for multiple forbidden." && exit 1
  fi
else
  echo "Test 11 Failed: Script passed unexpectedly." && exit 1
fi

echo "All tests completed successfully."
