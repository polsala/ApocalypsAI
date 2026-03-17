#!/bin/bash

set -euo pipefail

IMAGE_NAME="wasteland-recipe-replicator-test"

echo "Building Docker image..."
docker build -t "$IMAGE_NAME" .

# Mock rationale: The recipes.json is bundled within the Docker image, 
# so we are testing the container's ability to read its internal files 
# and process inputs, rather than mocking external file system interactions.

# Test Case 1: No ingredients provided
echo "\n--- Test Case 1: No ingredients ---"
OUTPUT=$(docker run "$IMAGE_NAME" --ingredients "")
EXPECTED_OUTPUT="[]"
if [[ "$OUTPUT" == "$EXPECTED_OUTPUT" ]]; then
  echo "PASS: No ingredients returned empty list."
else
  echo "FAIL: No ingredients. Expected '$EXPECTED_OUTPUT', got '$OUTPUT'"
  exit 1
fi

# Test Case 2: Ingredients for one recipe (Fungus & Bread Gruel)
echo "\n--- Test Case 2: Fungus & Bread Gruel ---"
OUTPUT=$(docker run "$IMAGE_NAME" --ingredients "mutant fungus,stale bread,purified water")
if echo "$OUTPUT" | grep -q "Fungus & Bread Gruel"; then
  echo "PASS: Found Fungus & Bread Gruel."
else
  echo "FAIL: Did not find Fungus & Bread Gruel. Output: $OUTPUT"
  exit 1
fi

# Test Case 3: Ingredients for another recipe (Radroach Skewers)
echo "\n--- Test Case 3: Radroach Skewers ---"
OUTPUT=$(docker run "$IMAGE_NAME" --ingredients "radroach meat,wild herbs,firewood")
if echo "$OUTPUT" | grep -q "Radroach Skewers"; then
  echo "PASS: Found Radroach Skewers."
else
  echo "FAIL: Did not find Radroach Skewers. Output: $OUTPUT"
  exit 1
fi

# Test Case 4: Ingredients for no known recipe
echo "\n--- Test Case 4: No matching recipe ---"
OUTPUT=$(docker run "$IMAGE_NAME" --ingredients "unknown berry,strange leaf")
EXPECTED_OUTPUT="[]"
if [[ "$OUTPUT" == "$EXPECTED_OUTPUT" ]]; then
  echo "PASS: No matching recipe returned empty list."
else
  echo "FAIL: No matching recipe. Expected '$EXPECTED_OUTPUT', got '$OUTPUT'"
  exit 1
fi

# Test Case 5: Partial ingredients (should not match)
echo "\n--- Test Case 5: Partial ingredients (should not match) ---"
OUTPUT=$(docker run "$IMAGE_NAME" --ingredients "mutant fungus,stale bread")
EXPECTED_OUTPUT="[]"
if [[ "$OUTPUT" == "$EXPECTED_OUTPUT" ]]; then
  echo "PASS: Partial ingredients returned empty list."
else
  echo "FAIL: Partial ingredients. Expected '$EXPECTED_OUTPUT', got '$OUTPUT'"
  exit 1
fi

# Test Case 6: Case insensitivity
echo "\n--- Test Case 6: Case insensitivity ---"
OUTPUT=$(docker run "$IMAGE_NAME" --ingredients "Mutant Fungus,Stale Bread,Purified Water")
if echo "$OUTPUT" | grep -q "Fungus & Bread Gruel"; then
  echo "PASS: Case insensitivity handled correctly."
else
  echo "FAIL: Case insensitivity failed. Output: $OUTPUT"
  exit 1
fi

# Test Case 7: Multiple matching recipes (if applicable, or just ensure one doesn't break others)
# This test case implicitly checks if the system can find one recipe without being confused by others.
# For this set of recipes, no single input set matches multiple recipes, so we'll re-verify a single match.
echo "\n--- Test Case 7: Verify single match with other recipes present ---"
OUTPUT=$(docker run "$IMAGE_NAME" --ingredients "mystery meat,root vegetables,purified water,salt")
if echo "$OUTPUT" | grep -q "Wasteland Stew"; then
  echo "PASS: Found Wasteland Stew correctly."
else
  echo "FAIL: Did not find Wasteland Stew. Output: $OUTPUT"
  exit 1
fi

echo "\nAll tests completed."

# Clean up the test image
docker rmi "$IMAGE_NAME" > /dev/null 2>&1 || true
