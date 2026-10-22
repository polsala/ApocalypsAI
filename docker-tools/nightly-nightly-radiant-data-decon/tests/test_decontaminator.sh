#!/bin/bash

set -euo pipefail

IMAGE_NAME="radiant-data-decon-test"
INPUT_DIR="./test_input"
OUTPUT_DIR="./test_output"

# Mock rationale: We create specific input files and define expected output files
# to simulate real-world contamination and verify the cleaning process deterministically.
# This avoids external dependencies and ensures repeatable tests.

cleanup() {
    echo "Cleaning up..."
    docker rmi -f "$IMAGE_NAME" > /dev/null 2>&1 || true
    rm -rf "$INPUT_DIR" "$OUTPUT_DIR"
}

trap cleanup EXIT

echo "--- Setting up test environment ---"
mkdir -p "$INPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Create a contaminated input file
cat <<EOF > "$INPUT_DIR/contaminated_log.txt"
Line 1 with   extra spaces.\x00\x01\x02

[ECHO] 2023-10-27 10:00:00 [ECHO] Some important data.
  Another line with \t tabs and trailing spaces.   
ERROR This is an error message.

EOF

# Define the expected cleaned output
cat <<EOF > "$OUTPUT_DIR/expected_cleaned_log.txt"
Line 1 with extra spaces.
Some important data.
Another line with tabs and trailing spaces.
This is an error message.
EOF

echo "--- Building Docker image ---"
docker build -t "$IMAGE_NAME" . > /dev/null

echo "--- Running decontaminator container ---"
docker run --rm \
  -v "$(pwd)/$INPUT_DIR:/app/input" \
  -v "$(pwd)/$OUTPUT_DIR:/app/output" \
  "$IMAGE_NAME" > /dev/null

echo "--- Verifying output ---"

if [ ! -f "$OUTPUT_DIR/contaminated_log.txt" ]; then
    echo "Error: Output file 'contaminated_log.txt' not found in $OUTPUT_DIR"
    exit 1
fi

# Compare the actual output with the expected output
diff -u "$OUTPUT_DIR/contaminated_log.txt" "$OUTPUT_DIR/expected_cleaned_log.txt"

if [ $? -eq 0 ]; then
    echo "Test passed: Output matches expected cleaned data."
else
    echo "Test failed: Output does not match expected cleaned data."
    exit 1
fi

cleanup
