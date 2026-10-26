#!/bin/bash

# Path to the script under test
SCRIPT_TO_TEST="../src/verify_tone.sh"

# Helper function to run the script and capture output/status
run_test() {
  local title="$1"
  local body="$2"
  local whimsy_kws="${3:-sparkle,giggle}"
  local doom_kws="${4:-apocalypse,void}"
  local min_whimsy="${5:-1}"
  local min_doom="${6:-1}"

  # Mock rationale: We are testing the script's logic in isolation.
  # We provide direct inputs as if they came from the GitHub Action.
  # No external services or files are accessed, ensuring determinism and offline execution.
  OUTPUT=$(bash "$SCRIPT_TO_TEST" "$title" "$body" "$whimsy_kws" "$doom_kws" "$min_whimsy" "$min_doom" 2>&1)
  EXIT_CODE=$?
  echo "$OUTPUT"
  return $EXIT_CODE
}

# Test Case 1: Perfect balance
echo "--- Test Case 1: Perfect balance ---"
OUTPUT=$(run_test "Add a joyful new feature" "This feature will bring delight to the post-apocalypse wasteland." "joyful,delight" "apocalypse,wasteland" "1" "1")
EXIT_CODE=$?
if [[ "$EXIT_CODE" -eq 0 && "$OUTPUT" =~ "status:pass" ]]; then
  echo "PASS: Perfect balance detected."
else
  echo "FAIL: Perfect balance not detected. Output: $OUTPUT, Exit: $EXIT_CODE"
  exit 1
fi

# Test Case 2: Missing whimsy
echo "--- Test Case 2: Missing whimsy ---"
OUTPUT=$(run_test "Fix critical bug in temporal anomaly" "This fix prevents a major void rift." "joyful,delight" "temporal,void" "1" "1")
EXIT_CODE=$?
if [[ "$EXIT_CODE" -eq 1 && "$OUTPUT" =~ "status:fail" && "$OUTPUT" =~ "Lacks sufficient whimsy" ]]; then
  echo "PASS: Missing whimsy detected."
else
  echo "FAIL: Missing whimsy not detected. Output: $OUTPUT, Exit: $EXIT_CODE"
  exit 1
fi

# Test Case 3: Missing doom
echo "--- Test Case 3: Missing doom ---"
OUTPUT=$(run_test "Implement a bubbly new UI" "Users will giggle with glee at this delightful interface." "bubbly,giggle" "temporal,void" "1" "1")
EXIT_CODE=$?
if [[ "$EXIT_CODE" -eq 1 && "$OUTPUT" =~ "status:fail" && "$OUTPUT" =~ "Lacks sufficient doom" ]]; then
  echo "PASS: Missing doom detected."
else
  echo "FAIL: Missing doom not detected. Output: $OUTPUT, Exit: $EXIT_CODE"
  exit 1
fi

# Test Case 4: Both missing
echo "--- Test Case 4: Both missing ---"
OUTPUT=$(run_test "Update dependencies" "Standard dependency update." "joyful,delight" "temporal,void" "1" "1")
EXIT_CODE=$?
if [[ "$EXIT_CODE" -eq 1 && "$OUTPUT" =~ "status:fail" && "$OUTPUT" =~ "Lacks sufficient whimsy" && "$OUTPUT" =~ "Lacks sufficient doom" ]]; then
  echo "PASS: Both missing detected."
else
  echo "FAIL: Both missing not detected. Output: $OUTPUT, Exit: $EXIT_CODE"
  exit 1
fi

# Test Case 5: Case insensitivity
echo "--- Test Case 5: Case insensitivity ---"
OUTPUT=$(run_test "A SPARKLE of hope in the VOID" "The APOCALYPSE is near, but we GIGGLE." "sparkle,giggle" "apocalypse,void" "1" "1")
EXIT_CODE=$?
if [[ "$EXIT_CODE" -eq 0 && "$OUTPUT" =~ "status:pass" ]]; then
  echo "PASS: Case insensitivity works."
else
  echo "FAIL: Case insensitivity failed. Output: $OUTPUT, Exit: $EXIT_CODE"
  exit 1
fi

# Test Case 6: Multiple keywords of same type
echo "--- Test Case 6: Multiple keywords of same type ---"
OUTPUT=$(run_test "A joyful and bubbly update" "This will delight users in the wasteland." "joyful,bubbly,delight" "wasteland" "2" "1")
EXIT_CODE=$?
if [[ "$EXIT_CODE" -eq 0 && "$OUTPUT" =~ "status:pass" ]]; then
  echo "PASS: Multiple keywords of same type counted correctly."
else
  echo "FAIL: Multiple keywords of same type failed. Output: $OUTPUT, Exit: $EXIT_CODE"
  exit 1
fi

# Test Case 7: No keywords, but min counts are 0
echo "--- Test Case 7: No keywords, but min counts are 0 ---"
OUTPUT=$(run_test "Simple update" "Just a regular change." "joyful,delight" "temporal,void" "0" "0")
EXIT_CODE=$?
if [[ "$EXIT_CODE" -eq 0 && "$OUTPUT" =~ "status:pass" ]]; then
  echo "PASS: No keywords, min counts 0 passed."
else
  echo "FAIL: No keywords, min counts 0 failed. Output: $OUTPUT, Exit: $EXIT_CODE"
  exit 1
fi

# Test Case 8: Keyword with special regex chars (should be handled by bash =~)
echo "--- Test Case 8: Keyword with special regex chars ---"
OUTPUT=$(run_test "Fix a [bug] in the void" "This is a [critical] fix." "bug" "[void]" "1" "1")
EXIT_CODE=$?
if [[ "$EXIT_CODE" -eq 0 && "$OUTPUT" =~ "status:pass" ]]; then
  echo "PASS: Keyword with special regex chars handled."
else
  echo "FAIL: Keyword with special regex chars failed. Output: $OUTPUT, Exit: $EXIT_CODE"
  exit 1
fi

echo "All tests completed."
