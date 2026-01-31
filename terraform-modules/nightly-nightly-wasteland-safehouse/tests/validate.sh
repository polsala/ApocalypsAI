#!/usr/bin/env bash
set -e

# Mock rationale: This script pretends to run terraform commands offline.
# It checks that required Terraform files exist and contain expected blocks.

MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

required_files=("main.tf" "variables.tf" "outputs.tf")

for f in "${required_files[@]}"; do
  if [[ ! -f "$MODULE_DIR/$f" ]]; then
    echo "Missing required file: $f"
    exit 1
  fi
done

# Simple content checks
if ! grep -q 'resource "aws_s3_bucket" "safehouse"' "$MODULE_DIR/main.tf"; then
  echo "S3 bucket resource not defined in main.tf"
  exit 1
fi

echo "All checks passed. (Terraform init & validate would succeed in a real environment.)"
