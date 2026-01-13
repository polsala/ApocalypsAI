#!/usr/bin/env bash
set -e

# Verify that all required Terraform files exist
required_files=("src/main.tf" "src/variables.tf" "src/outputs.tf")
for f in "${required_files[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "Missing required file: $f"
    exit 1
  fi
done

# Check that main.tf defines the aws_s3_bucket resource
if ! grep -q 'resource "aws_s3_bucket"' src/main.tf; then
  echo "aws_s3_bucket resource not found in src/main.tf"
  exit 1
fi

# Check that variables.tf defines bucket_name variable
if ! grep -q 'variable "bucket_name"' src/variables.tf; then
  echo "bucket_name variable not defined in src/variables.tf"
  exit 1
fi

# Simple sanity check for outputs
if ! grep -q 'output "website_endpoint"' src/outputs.tf; then
  echo "website_endpoint output missing in src/outputs.tf"
  exit 1
fi

echo "All checks passed. Terraform module structure looks good."

