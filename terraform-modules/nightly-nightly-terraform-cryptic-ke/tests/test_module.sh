#!/usr/bin/env bash
# test_module.sh – verifies that the Terraform module contains the required blocks.
# Mock rationale: we avoid invoking the real Terraform binary to keep the test offline and deterministic.

set -euo pipefail

# Helper to assert a pattern exists in a file.
assert_grep() {
  local pattern="$1"
  local file="$2"
  if ! grep -qE "$pattern" "$file"; then
    echo "FAIL: Expected pattern '$pattern' not found in $file"
    exit 1
  fi
}

# Check that the required provider block is present.
assert_grep "required_providers" "main.tf"
assert_grep "random" "main.tf"

# Check that the random_pet resource is defined.
assert_grep "resource \"random_pet\"" "main.tf"

# Check that the output is declared.
assert_grep "output \"vault_name\"" "outputs.tf"

echo "PASS: All required Terraform blocks are present."
