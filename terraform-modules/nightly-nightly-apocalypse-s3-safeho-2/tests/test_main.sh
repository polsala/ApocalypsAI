#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Ensure Terraform files contain required resources without invoking real Terraform.
# This test parses src/main.tf and checks for expected blocks.

TF_FILE="src/main.tf"

# Check that the file exists
if [[ ! -f "$TF_FILE" ]]; then
  echo "FAIL: $TF_FILE not found"
  exit 1
fi

# Check for aws_s3_bucket resource
if ! grep -q 'resource "aws_s3_bucket" "safehouse"' "$TF_FILE"; then
  echo "FAIL: aws_s3_bucket resource not defined"
  exit 1
fi

# Check versioning enabled
if ! grep -q -P 'versioning\s*\{[^}]*enabled\s*=\s*true' "$TF_FILE"; then
  echo "FAIL: versioning not enabled"
  exit 1
fi

# Check server_side_encryption_configuration present
if ! grep -q 'server_side_encryption_configuration' "$TF_FILE"; then
  echo "FAIL: server_side_encryption_configuration missing"
  exit 1
fi

# Check lifecycle_rule with expiration days = 30
if ! grep -q -P 'expiration\s*\{[^}]*days\s*=\s*30' "$TF_FILE"; then
  echo "FAIL: lifecycle expiration not set to 30 days"
  exit 1
fi

echo "PASS"
