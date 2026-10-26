#!/bin/bash

set -euo pipefail

echo "--- Running Terraform module tests ---"

# Navigate to the test directory
cd "$(dirname "$0")"

# Initialize Terraform
echo "Initializing Terraform..."
terraform init -backend=false # Mock rationale: Disable backend to prevent state file creation and cloud interaction.
if [ $? -ne 0 ]; then
  echo "Terraform init failed!"
  exit 1
fi
echo "Terraform init successful."

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate
if [ $? -ne 0 ]; then
  echo "Terraform validation failed!"
  exit 1
fi
echo "Terraform validation successful."

# Plan the Terraform configuration (without applying)
# This checks if the module can generate a valid plan with the given inputs.
echo "Planning Terraform configuration..."
terraform plan -var="aws_region=us-east-1" -out=tfplan.out
if [ $? -ne 0 ]; then
  echo "Terraform plan failed!"
  exit 1
fi
echo "Terraform plan successful. Plan saved to tfplan.out"

# Clean up the plan file
rm tfplan.out

echo "All Terraform module tests passed successfully!"
