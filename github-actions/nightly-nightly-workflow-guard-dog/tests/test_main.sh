#!/bin/bash

set -euo pipefail

# Mock the inputs for testing
_mock_input() {
  local name="$1"
  local value="$2"
  eval "INPUTS_${name}=\"$value\""
}

# Mock the inputs for the script
_mock_input "forbidden_patterns" "rm -rf /\ngit push --force"
_mock_input "fail_on_detection" "true"

# Source the main script to use its functions and variables
# We need to simulate the environment where the script runs, including inputs.
# This is a bit of a hacky way to test shell scripts with inputs.
# A more robust solution might involve a test runner or a dedicated testing framework.

# Create a temporary script that sets the inputs and then calls the main script
TEMP_SCRIPT=$(mktemp)
echo "#!/bin/bash" > "$TEMP_SCRIPT"
echo "set -euo pipefail" >> "$TEMP_SCRIPT"
echo "FORBIDDEN_PATTERNS=\"${INPUTS_forbidden_patterns}\"" >> "$TEMP_SCRIPT"
echo "FAIL_ON_DETECTION=\"${INPUTS_fail_on_detection}\"" >> "$TEMP_SCRIPT"

# Read the content of the main script and append it
cat src/main.sh >> "$TEMP_SCRIPT"

chmod +x "$TEMP_SCRIPT"

# --- Test Cases ---

# Test 1: Forbidden patterns detected, fail_on_detection is true
echo "--- Test 1: Forbidden patterns detected, fail_on_detection is true ---"
if "$TEMP_SCRIPT"; then
  echo "Test 1 FAILED: Expected script to exit with 1, but it succeeded."
  exit 1
else
  echo "Test 1 PASSED: Script correctly exited with 1."
fi

# Test 2: No forbidden patterns, should succeed
echo "--- Test 2: No forbidden patterns, should succeed ---"
_mock_input "forbidden_patterns" "# This is a comment\n# Another comment"
_mock_input "fail_on_detection" "true"

# Recreate temp script with new inputs
TEMP_SCRIPT_2=$(mktemp)
echo "#!/bin/bash" > "$TEMP_SCRIPT_2"
echo "set -euo pipefail" >> "$TEMP_SCRIPT_2"
echo "FORBIDDEN_PATTERNS=\"${INPUTS_forbidden_patterns}\"" >> "$TEMP_SCRIPT_2"
echo "FAIL_ON_DETECTION=\"${INPUTS_fail_on_detection}\"" >> "$TEMP_SCRIPT_2"
cat src/main.sh >> "$TEMP_SCRIPT_2"
chmod +x "$TEMP_SCRIPT_2"

if "$TEMP_SCRIPT_2"; then
  echo "Test 2 PASSED: Script succeeded as expected."
else
  echo "Test 2 FAILED: Script exited with 1 unexpectedly."
  exit 1
fi

# Test 3: Forbidden patterns detected, fail_on_detection is false
echo "--- Test 3: Forbidden patterns detected, fail_on_detection is false ---"
_mock_input "forbidden_patterns" "rm -rf /"
_mock_input "fail_on_detection" "false"

# Recreate temp script with new inputs
TEMP_SCRIPT_3=$(mktemp)
echo "#!/bin/bash" > "$TEMP_SCRIPT_3"
echo "set -euo pipefail" >> "$TEMP_SCRIPT_3"
echo "FORBIDDEN_PATTERNS=\"${INPUTS_forbidden_patterns}\"" >> "$TEMP_SCRIPT_3"
echo "FAIL_ON_DETECTION=\"${INPUTS_fail_on_detection}\"" >> "$TEMP_SCRIPT_3"
cat src/main.sh >> "$TEMP_SCRIPT_3"
chmod +x "$TEMP_SCRIPT_3"

if "$TEMP_SCRIPT_3"; then
  echo "Test 3 PASSED: Script succeeded as expected (warning only)."
else
  echo "Test 3 FAILED: Script exited with 1 unexpectedly."
  exit 1
fi

# Test 4: Empty forbidden patterns
echo "--- Test 4: Empty forbidden patterns ---"
_mock_input "forbidden_patterns" ""
_mock_input "fail_on_detection" "true"

# Recreate temp script with new inputs
TEMP_SCRIPT_4=$(mktemp)
echo "#!/bin/bash" > "$TEMP_SCRIPT_4"
echo "set -euo pipefail" >> "$TEMP_SCRIPT_4"
echo "FORBIDDEN_PATTERNS=\"${INPUTS_forbidden_patterns}\"" >> "$TEMP_SCRIPT_4"
echo "FAIL_ON_DETECTION=\"${INPUTS_fail_on_detection}\"" >> "$TEMP_SCRIPT_4"
cat src/main.sh >> "$TEMP_SCRIPT_4"
chmod +x "$TEMP_SCRIPT_4"

if "$TEMP_SCRIPT_4"; then
  echo "Test 4 PASSED: Script succeeded as expected (no patterns to check)."
else
  echo "Test 4 FAILED: Script exited with 1 unexpectedly."
  exit 1
fi

# Clean up temporary scripts
rm -f "$TEMP_SCRIPT" "$TEMP_SCRIPT_2" "$TEMP_SCRIPT_3" "$TEMP_SCRIPT_4"

echo "All tests completed."
exit 0
