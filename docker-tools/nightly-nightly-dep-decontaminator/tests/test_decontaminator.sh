#!/bin/bash

set -euo pipefail

IMAGE_NAME="nightly-dep-decontaminator-test"
TEMP_DIR="temp_project_for_test"

# Mock rationale: We are testing the Docker container's ability to process requirements.txt
# and report based on its internal config. We mock the input requirements.txt files
# and check the container's stdout for expected messages. This makes the test deterministic
# and offline, as it doesn't require actual package installations or network access.

cleanup() {
    echo "Cleaning up..."
    docker rmi "$IMAGE_NAME" || true
    rm -rf "$TEMP_DIR" || true
}

trap cleanup EXIT

echo "--- Building Docker image for testing ---"
docker build -t "$IMAGE_NAME" . > /dev/null

echo "--- Test Case 1: No requirements.txt ---"
rm -rf "$TEMP_DIR" && mkdir "$TEMP_DIR"
OUTPUT=$(docker run --rm -v "$(pwd)/$TEMP_DIR:/app/project" "$IMAGE_NAME" 2>&1)
if echo "$OUTPUT" | grep -q "Warning: requirements.txt not found"; then
    echo "✅ Test Case 1 Passed: Handled missing requirements.txt"
else
    echo "❌ Test Case 1 Failed: Did not handle missing requirements.txt"
    echo "Output: $OUTPUT"
    exit 1
fi

echo "--- Test Case 2: Empty requirements.txt ---"
rm -rf "$TEMP_DIR" && mkdir "$TEMP_DIR"
touch "$TEMP_DIR/requirements.txt"
OUTPUT=$(docker run --rm -v "$(pwd)/$TEMP_DIR:/app/project" "$IMAGE_NAME" 2>&1)
if echo "$OUTPUT" | grep -q "No dependencies found or requirements.txt is missing/empty. All clear!"; then
    echo "✅ Test Case 2 Passed: Handled empty requirements.txt"
else
    echo "❌ Test Case 2 Failed: Did not handle empty requirements.txt"
    echo "Output: $OUTPUT"
    exit 1
fi

echo "--- Test Case 3: Lean requirements.txt ---"
rm -rf "$TEMP_DIR" && mkdir "$TEMP_DIR"
cat <<EOF > "$TEMP_DIR/requirements.txt"
requests-toolbelt
beautifulsoup4
click
EOF
OUTPUT=$(docker run --rm -v "$(pwd)/$TEMP_DIR:/app/project" "$IMAGE_NAME" 2>&1)
if echo "$OUTPUT" | grep -q "All dependencies appear lean and essential for survival. Good job!"; then
    echo "✅ Test Case 3 Passed: Identified lean dependencies"
else
    echo "❌ Test Case 3 Failed: Did not identify lean dependencies correctly"
    echo "Output: $OUTPUT"
    exit 1
fi

echo "--- Test Case 4: Heavy and Unnecessary requirements.txt ---"
rm -rf "$TEMP_DIR" && mkdir "$TEMP_DIR"
cat <<EOF > "$TEMP_DIR/requirements.txt"
Django==3.2.5
numpy>=1.20.0
pytest
requests
# A comment line
tensorflow
EOF
OUTPUT=$(docker run --rm -v "$(pwd)/$TEMP_DIR:/app/project" "$IMAGE_NAME" 2>&1)
if echo "$OUTPUT" | grep -q "🚨 HEAVY DEPENDENCY DETECTED: 'django'" && \
   echo "$OUTPUT" | grep -q "🚨 HEAVY DEPENDENCY DETECTED: 'numpy'" && \
   echo "$OUTPUT" | grep -q "⚠️ UNNECESSARY DEPENDENCY DETECTED: 'pytest'" && \
   echo "$OUTPUT" | grep -q "🚨 HEAVY DEPENDENCY DETECTED: 'requests'" && \
   echo "$OUTPUT" | grep -q "🚨 HEAVY DEPENDENCY DETECTED: 'tensorflow'"; then
    echo "✅ Test Case 4 Passed: Identified heavy and unnecessary dependencies"
else
    echo "❌ Test Case 4 Failed: Did not identify heavy and unnecessary dependencies correctly"
    echo "Output: $OUTPUT"
    exit 1
fi

echo "--- Test Case 5: Requirements with different specifiers ---"
rm -rf "$TEMP_DIR" && mkdir "$TEMP_DIR"
cat <<EOF > "$TEMP_DIR/requirements.txt"
pandas~=1.3.0
black==22.3.0
scipy>1.5.0
EOF
OUTPUT=$(docker run --rm -v "$(pwd)/$TEMP_DIR:/app/project" "$IMAGE_NAME" 2>&1)
if echo "$OUTPUT" | grep -q "🚨 HEAVY DEPENDENCY DETECTED: 'pandas'" && \
   echo "$OUTPUT" | grep -q "⚠️ UNNECESSARY DEPENDENCY DETECTED: 'black'" && \
   echo "$OUTPUT" | grep -q "🚨 HEAVY DEPENDENCY DETECTED: 'scipy'"; then
    echo "✅ Test Case 5 Passed: Handled different version specifiers"
else
    echo "❌ Test Case 5 Failed: Did not handle different version specifiers correctly"
    echo "Output: $OUTPUT"
    exit 1
fi

echo "All tests passed!"
