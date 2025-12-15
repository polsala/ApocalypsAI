#!/bin/bash
set -euo pipefail

echo "-- Running Terraform tests for nightly-temporal-echo-chamber-tf --"

# Navigate to the test directory
cd "$(dirname "$0")"

# Initialize Terraform in the test directory
echo "Initializing Terraform..."
# -backend=false: Prevents Terraform from trying to configure a state backend, making the test offline.
# -input=false: Prevents Terraform from prompting for input.
terraform init -backend=false -input=false

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Plan the Terraform configuration without applying
# We provide dummy variables for required inputs to allow plan to proceed without real AWS calls.
# Mock rationale: `terraform plan` is used here to validate the module's syntax and variable usage.
# By providing dummy values for `ami_id` and `aws_region`, the plan can be generated without requiring
# actual AWS credentials or a valid AMI, making the test deterministic and offline.
echo "Planning Terraform configuration (no actual resources will be created)..."
terraform plan -out=tfplan \
  -var "aws_region=us-east-1" \
  -var "ami_id=ami-0abcdef1234567890" \
  -var "instance_type=t2.micro" \
  -var "duration_minutes=5" \
  -input=false

# Check if the plan file was created
if [ -f "tfplan" ]; then
  echo "Terraform plan created successfully. Test passed."
  rm tfplan # Clean up the plan file
else
  echo "Error: Terraform plan file was not created. Test failed."
  exit 1
fi

echo "-- All Terraform tests passed! --"
