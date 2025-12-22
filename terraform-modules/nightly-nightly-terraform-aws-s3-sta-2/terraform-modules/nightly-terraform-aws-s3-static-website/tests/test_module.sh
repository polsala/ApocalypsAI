#!/usr/bin/env bash
set -e

# Mock rationale: This test runs Terraform in a temporary directory without any remote backend.
# It validates the configuration and checks that the expected S3 bucket resource is defined.

MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"

# Initialize Terraform (backend disabled to keep it offline)
terraform -chdir="$MODULE_DIR" init -backend=false > /dev/null

# Validate the configuration syntax
terraform -chdir="$MODULE_DIR" validate

# Ensure the S3 bucket resource is present in the module
if ! grep -q "resource \"aws_s3_bucket\"" "$MODULE_DIR/main.tf"; then
  echo "❌ Expected aws_s3_bucket resource not found in main.tf"
  exit 1
fi

# Ensure website configuration block exists
if ! grep -q "resource \"aws_s3_bucket_website_configuration\"" "$MODULE_DIR/main.tf"; then
  echo "❌ Expected aws_s3_bucket_website_configuration resource not found in main.tf"
  exit 1
fi

echo "✅ All Terraform module tests passed"
