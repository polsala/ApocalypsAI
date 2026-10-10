#!/bin/bash

set -euo pipefail

# Mock rationale: We create temporary files to simulate the repository's file system
# and control their content for deterministic testing of grep patterns.
# The 'date' command is mocked by explicitly setting INPUT_CURRENT_YEAR.
# GITHUB_OUTPUT is mocked by redirecting its output to a temporary file.

# Function to parse GITHUB_OUTPUT
parse_github_output() {
  local output_file="$1"
  local key="$2"
  local value=""
  local in_multiline="false"
  local delimiter=""

  while IFS= read -r line; do
    if [[ "$in_multiline" == "true" ]]; then
      if [[ "$line" == "$delimiter" ]]; then
        in_multiline="false"
        break
      else
        value+="$line\n"
      fi
    elif [[ "$line" == "$key<<"* ]]; then
      delimiter="${line#*<<}"
      in_multiline="true"
    elif [[ "$line" == "$key="* ]]; then
      value="${line#*=}"
      break
    fi
  done < "$output_file"
  # Remove trailing newline for multiline values if it was a multiline block
  if [[ "$in_multiline" == "false" && -n "$value" ]]; then
    echo -e "${value%\\n}"
  else
    echo -e "$value"
  fi
}


# Setup: Create a temporary directory for testing
TEST_DIR=$(mktemp -d)
cd "$TEST_DIR"

# Mock GITHUB_OUTPUT
MOCK_GITHUB_OUTPUT=$(mktemp)
export GITHUB_OUTPUT="$MOCK_GITHUB_OUTPUT"

# Mock github.action_path for the script to find itself
export github_action_path="$(pwd)/.."

# --- Test Case 1: No outdated years --- (Current year is 2024, files contain 2024)
echo "Running Test Case 1: No outdated years"
mkdir -p src
echo "Copyright 2024" > src/file1.txt
echo "License 2024" > LICENSE
echo "Current year is 2024" > README.md

export INPUT_GITHUB_TOKEN="mock_token"
export INPUT_SCAN_PATHS="src/file1.txt,LICENSE,README.md"
export INPUT_CURRENT_YEAR="2024"

bash ../src/main.sh

ANOMALIES_FOUND=$(parse_github_output "$MOCK_GITHUB_OUTPUT" "anomalies-found")
REPORT=$(parse_github_output "$MOCK_GITHUB_OUTPUT" "report")

if [ "$ANOMALIES_FOUND" != "false" ]; then
  echo "Test Case 1 FAILED: anomalies-found was '$ANOMALIES_FOUND', expected 'false'"
  exit 1
fi
if ! echo "$REPORT" | grep -q "No temporal anomalies"; then
  echo "Test Case 1 FAILED: Report did not indicate no anomalies."
  echo "Report content:" && echo "$REPORT"
  exit 1
fi
echo "Test Case 1 PASSED"

# Clean up for next test case
rm -f "$MOCK_GITHUB_OUTPUT"
> "$MOCK_GITHUB_OUTPUT" # Clear the mock output file

# --- Test Case 2: Outdated year in a file --- (Current year is 2024, file contains 2023)
echo "Running Test Case 2: Outdated year in a file"
echo "Copyright 2023" > src/file2.txt # Outdated
echo "License 2024" > LICENSE
echo "Current year is 2024" > README.md

export INPUT_SCAN_PATHS="src/file2.txt,LICENSE,README.md"
export INPUT_CURRENT_YEAR="2024"

bash ../src/main.sh

ANOMALIES_FOUND=$(parse_github_output "$MOCK_GITHUB_OUTPUT" "anomalies-found")
REPORT=$(parse_github_output "$MOCK_GITHUB_OUTPUT" "report")

if [ "$ANOMALIES_FOUND" != "true" ]; then
  echo "Test Case 2 FAILED: anomalies-found was '$ANOMALIES_FOUND', expected 'true'"
  exit 1
fi
if ! echo "$REPORT" | grep -q "File: \`src/file2.txt\`: Detected an outdated year (\`2023\`). Consider updating to \`2024\`"; then
  echo "Test Case 2 FAILED: Report did not mention outdated year in src/file2.txt."
  echo "Report content:" && echo "$REPORT"
  exit 1
fi
echo "Test Case 2 PASSED"

# Clean up for next test case
rm -f "$MOCK_GITHUB_OUTPUT"
> "$MOCK_GITHUB_OUTPUT" # Clear the mock output file

# --- Test Case 3: Outdated year in a directory --- (Current year is 2024, doc1.md contains 2023)
echo "Running Test Case 3: Outdated year in a directory"
mkdir -p docs
echo "Documentation 2023" > docs/doc1.md # Outdated
echo "Another doc 2024" > docs/doc2.md
echo "Copyright 2024" > src/file3.txt

export INPUT_SCAN_PATHS="docs/,src/file3.txt"
export INPUT_CURRENT_YEAR="2024"

bash ../src/main.sh

ANOMALIES_FOUND=$(parse_github_output "$MOCK_GITHUB_OUTPUT" "anomalies-found")
REPORT=$(parse_github_output "$MOCK_GITHUB_OUTPUT" "report")

if [ "$ANOMALIES_FOUND" != "true" ]; then
  echo "Test Case 3 FAILED: anomalies-found was '$ANOMALIES_FOUND', expected 'true'"
  exit 1
fi
if ! echo "$REPORT" | grep -q "File: \`docs/doc1.md\`: Detected an outdated year (\`2023\`). Consider updating to \`2024\`"; then
  echo "Test Case 3 FAILED: Report did not mention outdated year in docs/doc1.md."
  echo "Report content:" && echo "$REPORT"
  exit 1
fi
echo "Test Case 3 PASSED"

# Clean up
cd - > /dev/null # Go back to original directory
rm -rf "$TEST_DIR"
rm -f "$MOCK_GITHUB_OUTPUT"

echo "All tests PASSED!"
