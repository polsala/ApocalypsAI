#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Run terraform init and validate locally without contacting AWS.
terraform init -backend=false > /dev/null
terraform validate

# Ensure plan contains the bucket resource
plan_output=$(terraform plan -no-color -input=false)
echo "$plan_output" | grep -q "aws_s3_bucket.supply_bucket"
echo "All tests passed."
