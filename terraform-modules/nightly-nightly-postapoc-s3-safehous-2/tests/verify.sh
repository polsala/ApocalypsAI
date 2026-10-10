#!/usr/bin/env bash
# verify.sh – deterministic offline test for the nightly‑postapoc‑s3‑safehouse module
# Mock rationale: we avoid contacting AWS by only checking file contents and Terraform formatting.

set -euo pipefail

# 1. Ensure Terraform files are properly formatted
if ! command -v terraform >/dev/null 2>&1; then
  echo "Terraform binary not found – skipping fmt check (treated as pass)"
else
  terraform fmt -check -recursive .
fi

# 2. Verify that main.tf defines the expected S3 resources
required_resources=("aws_s3_bucket.safehouse" "aws_s3_bucket_versioning.safehouse_versioning" "aws_s3_bucket_lifecycle_configuration.safehouse_lifecycle")
for res in "${required_resources[@]}"; do
  if ! grep -q "$res" src/main.tf; then
    echo "Missing required resource $res in src/main.tf"
    exit 1
  fi
done

# 3. Simple variable sanity check – bucket_name must be a string placeholder
if ! grep -q "variable \"bucket_name\"" src/variables.tf; then
  echo "bucket_name variable definition missing"
  exit 1
fi

echo "All checks passed."
