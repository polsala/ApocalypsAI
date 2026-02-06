#!/usr/bin/env bash
# test_module.sh – verifies that the Terraform module contains expected blocks.
# Mock rationale: runs offline, uses grep to check file contents.

set -euo pipefail

MODULE_DIR="$(cd $(dirname $0)/../src && pwd)"

# Helper to assert a pattern exists in a file
assert_grep() {
  local pattern=$1
  local file=$2
  if ! grep -qE "$pattern" "$file"; then
    echo "FAIL: Expected pattern '$pattern' not found in $file"
    exit 1
  fi
}

# Check variables.tf for required variables
assert_grep "variable \"bucket_name\"" "$MODULE_DIR/variables.tf"
assert_grep "variable \"enable_cdn\"" "$MODULE_DIR/variables.tf"
assert_grep "variable \"index_document\"" "$MODULE_DIR/variables.tf"
assert_grep "variable \"error_document\"" "$MODULE_DIR/variables.tf"

# Check main.tf for S3 bucket resource
assert_grep "resource \"aws_s3_bucket\" \"static_site\"" "$MODULE_DIR/main.tf"
assert_grep "website \{" "$MODULE_DIR/main.tf"

# Check optional CloudFront block exists (conditional count)
assert_grep "resource \"aws_cloudfront_distribution\" \"cdn\"" "$MODULE_DIR/main.tf"
assert_grep "count = var.enable_cdn \? 1 : 0" "$MODULE_DIR/main.tf"

# Check outputs.tf for expected outputs
assert_grep "output \"bucket_id\"" "$MODULE_DIR/outputs.tf"
assert_grep "output \"bucket_arn\"" "$MODULE_DIR/outputs.tf"
assert_grep "output \"cloudfront_domain\"" "$MODULE_DIR/outputs.tf"

echo "All checks passed."
