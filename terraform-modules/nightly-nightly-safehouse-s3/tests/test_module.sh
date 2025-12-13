#!/usr/bin/env bash
set -e

# Mock rationale: Ensure the Terraform module contains expected resources and configurations.

# Resolve the directory of this script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MODULE_DIR="$SCRIPT_DIR/../src"

# Check that main.tf defines an aws_s3_bucket resource
if ! grep -q 'resource "aws_s3_bucket" "safehouse"' "$MODULE_DIR/main.tf"; then
  echo "Missing aws_s3_bucket resource"
  exit 1
fi

# Check that versioning is enabled
if ! grep -q 'versioning {' "$MODULE_DIR/main.tf"; then
  echo "Missing versioning block"
  exit 1
fi

# Check that lifecycle expiration is set to 30 days
if ! grep -q 'days = 30' "$MODULE_DIR/main.tf"; then
  echo "Missing lifecycle expiration of 30 days"
  exit 1
fi

echo "All checks passed."
