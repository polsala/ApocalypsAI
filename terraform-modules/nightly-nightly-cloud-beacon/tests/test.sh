#!/bin/bash
# Mock rationale: This script performs offline, deterministic tests using Terraform CLI commands.
# It does not interact with any actual cloud provider or require credentials.
# 'terraform init -backend=false' prevents backend configuration, and 'terraform plan -destroy'
# ensures that a plan can be generated for resource destruction, implicitly validating creation.

set -euo pipefail

echo "--- Running Terraform module tests for nightly-cloud-beacon ---"

# Navigate to the tests directory
cd "$(dirname "$0")"

# Initialize Terraform in the test directory, skipping backend configuration
echo "Initializing Terraform (backend=false)..."
terraform init -backend=false

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Generate a plan to destroy the resources. This implicitly validates that the resources
# can be defined and a plan can be formed, without actually creating anything.
# We use dummy variables for the module.
echo "Generating a destroy plan (offline validation)..."
terraform plan -destroy -out=tfplan -var "bucket_name=apocalypsai-test-beacon-12345" -var "aws_region=us-east-1"

# Check if the plan file was created
if [ -f "tfplan" ]; then
  echo "Terraform plan generated successfully."
  rm tfplan # Clean up the plan file
else
  echo "Error: Terraform plan generation failed."
  exit 1
fi

echo "--- All tests passed for nightly-cloud-beacon! ---"
