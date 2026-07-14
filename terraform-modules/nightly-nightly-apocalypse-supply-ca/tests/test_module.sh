#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: This test verifies that the Terraform module files contain the expected resources and variables without invoking Terraform or external providers.

MODULE_DIR="$(dirname "${BASH_SOURCE[0]}")/.."

# Check main.tf for aws_s3_bucket resource
if ! grep -q 'resource "aws_s3_bucket" "supply_cache"' "$MODULE_DIR/main.tf"; then
  echo "FAIL: aws_s3_bucket resource not found in main.tf"
  exit 1
fi

# Check for versioning resource
if ! grep -q 'resource "aws_s3_bucket_versioning"' "$MODULE_DIR/main.tf"; then
  echo "FAIL: versioning resource not found"
  exit 1
fi

# Check for encryption resource
if ! grep -q 'resource "aws_s3_bucket_server_side_encryption_configuration"' "$MODULE_DIR/main.tf"; then
  echo "FAIL: encryption resource not found"
  exit 1
fi

# Check for lifecycle resource
if ! grep -q 'resource "aws_s3_bucket_lifecycle_configuration"' "$MODULE_DIR/main.tf"; then
  echo "FAIL: lifecycle resource not found"
  exit 1
fi

# Check variables.tf for bucket_name variable
if ! grep -q 'variable "bucket_name"' "$MODULE_DIR/variables.tf"; then
  echo "FAIL: bucket_name variable not defined"
  exit 1
fi

echo "PASS: All expected resources and variables are present."
