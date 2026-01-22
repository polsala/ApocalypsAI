#!/bin/bash
set -e

IMAGE_NAME="wasteland-scrubber-test"
INPUT_DIR="test_data/input"
OUTPUT_DIR="test_data/output"
EXPECTED_DIR="test_data/expected"

# Mock rationale: Creating dummy input files directly on the filesystem and comparing the container's
# output against a predefined expected output file ensures the test is deterministic and offline.
# No external services, network calls, or dynamic data generation are involved.

echo "-- Building Docker image --"
docker build -t "$IMAGE_NAME" src/

echo "-- Setting up test directories --"
mkdir -p "$INPUT_DIR" "$OUTPUT_DIR" "$EXPECTED_DIR"

# Create a mock input file for the scrubber
cat <<EOF > "$INPUT_DIR/raw_sensor_log.txt"
Sensor Log 234:
[ERROR] Corrupted signal detected.
DATA: [RESOURCE:Water] Amount: 10 units. Location: (COORD:34.56,-118.23)
Noise: asdfasdfasdf
DATA: [RESOURCE:Food] Amount: 5 rations. Location: (COORD:34.57,-118.24)
[WARNING] Battery low.
DATA: [RESOURCE:Scrap Metal] Amount: 15 kg. Location: (COORD:34.58,-118.25)
EOF

# Create the expected output file that the scrubber should produce
cat <<EOF > "$EXPECTED_DIR/cleaned_data.csv"
Resource,Amount,Location
Water,10,34.56,-118.23
Food,5,34.57,-118.24
Scrap Metal,15,34.58,-118.25
EOF

echo "-- Running scrubber container --"
# Run the Docker container, mounting the input and output directories
# The --rm flag ensures the container is removed after exit
docker run --rm \
  -v "$(pwd)/$INPUT_DIR:/input" \
  -v "$(pwd)/$OUTPUT_DIR:/output" \
  "$IMAGE_NAME" \
  --input /input/raw_sensor_log.txt \
  --output /output/cleaned_data.csv

echo "-- Verifying output --"
# Compare the generated output with the expected output
if diff -q "$OUTPUT_DIR/cleaned_data.csv" "$EXPECTED_DIR/cleaned_data.csv"; then
  echo "Test PASSED: Output matches expected."
else
  echo "Test FAILED: Output differs from expected."
  echo "-- Diff --"
  diff "$OUTPUT_DIR/cleaned_data.csv" "$EXPECTED_DIR/cleaned_data.csv"
  exit 1
fi

echo "-- Cleaning up --"
# Remove temporary test directories and the Docker image
rm -rf "$INPUT_DIR" "$OUTPUT_DIR" "$EXPECTED_DIR"
docker rmi "$IMAGE_NAME" > /dev/null 2>&1 || true # Ignore error if image is in use

echo "All tests completed successfully."
