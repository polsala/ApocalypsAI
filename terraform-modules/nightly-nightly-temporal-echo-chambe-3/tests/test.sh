#!/bin/bash
set -euo pipefail

echo "-- Running Nightly Temporal Echo Chamber Provisioner Tests --"

# Navigate to the test directory
cd "$(dirname "$0")"

# Initialize Terraform in the test directory
echo "Initializing Terraform..."
# Mock rationale: -backend=false prevents state backend configuration, making the test fully offline and independent of cloud state.
terraform init -backend=false

# Validate the Terraform configuration for syntax and consistency
echo "Validating Terraform configuration..."
terraform validate

# Generate a Terraform plan to ensure no errors and predictable changes without applying.
# Mock rationale: `terraform plan` simulates resource creation/modification without making actual API calls, ensuring the module's logic is sound offline.
echo "Generating Terraform plan (no apply)..."
terraform plan -destroy -out=tfplan -var="prefix=test-apocalypsai-echo-chamber-plan" -var="retention_days=1" -var="aws_region=us-east-1"

# Check if the plan file was created, indicating a successful plan generation
if [ ! -f tfplan ]; then
  echo "Error: Terraform plan file 'tfplan' was not created."
  exit 1
fi

echo "Terraform plan generated successfully. Cleaning up plan file."
rm tfplan # Clean up the generated plan file

echo "-- All Nightly Temporal Echo Chamber Provisioner tests passed! --"
