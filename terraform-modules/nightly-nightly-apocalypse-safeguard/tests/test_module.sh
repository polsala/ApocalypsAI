#!/usr/bin/env bash
set -e

# Mock rationale: Ensure required resources are defined in main.tf
MODULE_DIR="$(dirname "${BASH_SOURCE[0]}")/.."

if ! grep -q 'resource "aws_s3_bucket"' "$MODULE_DIR/main.tf"; then
  echo "Missing aws_s3_bucket resource"
  exit 1
fi

if ! grep -q 'versioning {' "$MODULE_DIR/main.tf"; then
  echo "Missing versioning block"
  exit 1
fi

if ! grep -q 'server_side_encryption_configuration' "$MODULE_DIR/main.tf"; then
  echo "Missing encryption configuration"
  exit 1
fi

echo "All checks passed"
