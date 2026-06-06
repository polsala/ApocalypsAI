#!/bin/bash

set -e # Exit immediately if a command exits with a non-zero status.

echo "Starting offline Terraform module tests for nightly-temporal-beacon..."

# Initialize Terraform in the test directory. Backend is disabled as no state needs to be managed.
echo "Initializing Terraform in test directory (backend disabled)..."
terraform -chdir=tests init -backend=false

# Run terraform plan to validate syntax and configuration without applying.
# Mock rationale: This test is offline and deterministic. It validates the Terraform module's syntax,
# variable definitions, and output declarations without deploying any actual AWS resources.
# The 'vpc_id' and 'public_subnet_ids' values are placeholders to satisfy variable requirements
# for 'terraform plan' and 'terraform output' commands, ensuring the module is syntactically correct
# and its outputs are accessible. The AWS provider is configured in tests/main.tf but no credentials
# are needed for 'plan' when no actual API calls are made.
echo "Running terraform plan to validate module syntax..."
terraform -chdir=tests plan -out=tfplan -var="vpc_id=vpc-mockid1234567890" -var="public_subnet_ids=["subnet-mockid1234567890a","subnet-mockid1234567890b"]"

# Check if the plan file was created, indicating a successful plan.
if [ ! -f "tests/tfplan" ]; then
  echo "Error: Terraform plan file (tfplan) was not created." >&2
  exit 1
fi

# Attempt to get an output, which also validates that outputs are correctly defined.
echo "Attempting to retrieve module output 'test_alb_dns'..."
ALB_DNS=$(terraform -chdir=tests output -raw test_alb_dns)

if [ -z "$ALB_DNS" ]; then
  echo "Error: Failed to retrieve 'test_alb_dns' output." >&2
  exit 1
fi

echo "Successfully retrieved mock ALB DNS: $ALB_DNS"

# Clean up the generated plan file.
echo "Cleaning up generated tfplan file..."
rm tests/tfplan

echo "All offline Terraform module tests passed successfully!"
