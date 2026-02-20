#!/bin/bash
set -euo pipefail

echo "--- Running Terraform module tests for nightly-wasteland-beacon ---"

# Change to the tests directory
SCRIPT_DIR=$(dirname "$(realpath "$0")")
cd "$SCRIPT_DIR"

# Initialize Terraform in the test directory
echo "Initializing Terraform..."
# Mock rationale: -backend=false prevents Terraform from trying to configure a remote state backend,
# ensuring the test is offline and self-contained.
terraform init -backend=false

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Generate a plan to ensure resources can be created without errors
echo "Generating Terraform plan..."
# Mock rationale: -out=plan.tfplan creates a plan file without applying,
# allowing inspection of the planned changes without actual cloud interaction.
# -var flags provide necessary input variables for the module.
terraform plan -out=plan.tfplan \
  -var 'beacon_name=test-wasteland-beacon' \
  -var 'schedule_expression=rate(1 hour)' \
  -var 'aws_region=us-east-1'

# Check if the plan command was successful
if [ $? -eq 0 ]; then
  echo "Terraform plan generated successfully."
  # Optional: Add assertions on the plan output using `terraform show -json plan.tfplan`
  # For this exercise, successful plan generation is sufficient for offline testing.
else
  echo "Terraform plan failed."
  exit 1
fi

echo "--- All Terraform module tests passed! ---"
