#!/usr/bin/env bash
set -e

# Initialize Terraform without a backend (local only)
terraform init -backend=false > /dev/null

# Validate the configuration syntax
terraform validate

# Generate a plan with a sample variable
terraform plan -var="bucket_name=testbucket" -out=plan.out > /dev/null

# Ensure the plan includes the expected local_file resource
if ! terraform show -json plan.out | grep -q '"type":"local_file"'; then
  echo "Plan does not contain local_file resource"
  exit 1
fi

echo "All tests passed."
