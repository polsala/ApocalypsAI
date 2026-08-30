#!/usr/bin/env bash
set -e

# Mock rationale: This test validates that the Terraform module contains required resources
# without invoking real AWS APIs. It checks for presence of resource blocks in main.tf.

MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Check that main.tf exists
if [[ ! -f "$MODULE_DIR/src/main.tf" ]]; then
  echo "FAIL: src/main.tf not found"
  exit 1
fi

# Verify required resources are defined
REQUIRED=("aws_s3_bucket" "aws_s3_bucket_versioning" "aws_s3_bucket_server_side_encryption_configuration" "aws_s3_bucket_lifecycle_configuration")
for RES in "${REQUIRED[@]}"; do
  if ! grep -q "resource \"${RES}\"" "$MODULE_DIR/src/main.tf"; then
    echo "FAIL: Resource ${RES} not found in main.tf"
    exit 1
  fi
done

echo "PASS: All required resources are present"
exit 0
