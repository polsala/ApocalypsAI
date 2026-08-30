#!/usr/bin/env bash
# Test script for nightly-safehouse-s3 Terraform module
# Mock rationale: The test runs entirely offline, checking that the expected
# resources and configurations are present in the Terraform files.

set -euo pipefail

# Helper to assert a pattern exists in a file
assert_in_file() {
  local pattern=$1
  local file=$2
  if ! grep -qE "$pattern" "$file"; then
    echo "FAIL: Expected pattern '$pattern' not found in $file"
    exit 1
  fi
}

# 1. Verify required provider block exists
assert_in_file "required_providers\s*{[^}]*aws" "main.tf"

# 2. Verify S3 bucket resource name and versioning enabled
assert_in_file "resource \"aws_s3_bucket\" \"safehouse\"" "main.tf"
assert_in_file "versioning \{[^}]*enabled\s*=\s*true" "main.tf"

# 3. Verify server‑side encryption configuration
assert_in_file "sse_algorithm\s*=\s*\"AES256\"" "main.tf"

# 4. Verify lifecycle rule with 30‑day expiration
assert_in_file "expiration \{[^}]*days\s*=\s*30" "main.tf"

# 5. Verify variables are declared
assert_in_file "variable \"bucket_name\"" "variables.tf"
assert_in_file "variable \"tags\"" "variables.tf"

# 6. Verify outputs are defined
assert_in_file "output \"bucket_id\"" "outputs.tf"
assert_in_file "output \"bucket_arn\"" "outputs.tf"

echo "PASS: All checks passed for nightly-safehouse-s3 module"
