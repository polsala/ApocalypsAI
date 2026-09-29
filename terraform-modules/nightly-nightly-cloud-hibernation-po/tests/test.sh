#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests..."

# Change to the test directory
cd "$(dirname "$0")"

# Initialize Terraform
echo "Initializing Terraform..."
terraform init -backend=false # Mock rationale: No actual state backend needed for plan/validate.
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

# Generate a plan (without applying)
echo "Generating Terraform plan..."
# -detailed-exitcode: 0=no changes, 1=error, 2=changes present
terraform plan -out=tfplan -detailed-exitcode
PLAN_EXIT_CODE=$?
if [ $PLAN_EXIT_CODE -eq 1 ]; then
  echo "Terraform plan generation failed!"
  exit 1
fi
if [ $PLAN_EXIT_CODE -eq 0 ]; then
  echo "Terraform plan shows no changes, which is unexpected for a new module. This might indicate an issue."
  exit 1
fi
echo "Terraform plan generated successfully (exit code: $PLAN_EXIT_CODE, indicating changes)."

echo "All Terraform tests passed!"
rm tfplan # Clean up the plan file
