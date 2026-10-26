#!/usr/bin/env bash
set -e

# Mock rationale: Use local backend to avoid remote state and ensure deterministic run.
terraform init -backend=false > /dev/null

# Validate configuration syntax
terraform validate

# Generate a plan without prompting for input
plan_output=$(terraform plan -input=false -no-color)

# Verify that the S3 bucket resource and required configurations exist
echo "$plan_output" | grep -q 'resource "aws_s3_bucket" "safehouse"'
echo "$plan_output" | grep -q 'versioning {'
echo "$plan_output" | grep -q 'server_side_encryption_configuration {'
echo "$plan_output" | grep -q 'lifecycle_rule {'

echo "All checks passed."
