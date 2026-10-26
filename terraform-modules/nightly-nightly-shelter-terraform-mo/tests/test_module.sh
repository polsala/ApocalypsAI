#!/usr/bin/env bash
set -e

# Mock rationale: Verify that the Terraform files contain the expected resources and variables.
# This avoids network calls and keeps the test deterministic.

MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Helper to assert a pattern exists in a file
assert_grep() {
  local pattern="$1"
  local file="$2"
  if ! grep -qE "$pattern" "$file"; then
    echo "FAIL: Expected pattern '$pattern' not found in $file"
    exit 1
  fi
}

# Check that main.tf defines the random_pet and aws_s3_bucket resources
assert_grep "resource \"random_pet\" \"shelter_name\"" "$MODULE_DIR/src/main.tf"
assert_grep "resource \"aws_s3_bucket\" \"shelter_bucket\"" "$MODULE_DIR/src/main.tf"

# Check that variables.tf defines bucket_name_prefix variable
assert_grep "variable \"bucket_name_prefix\"" "$MODULE_DIR/src/variables.tf"

# Check that outputs.tf defines bucket_name output
assert_grep "output \"bucket_name\"" "$MODULE_DIR/src/outputs.tf"

echo "All checks passed."
