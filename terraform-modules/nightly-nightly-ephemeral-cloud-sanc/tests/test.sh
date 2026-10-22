#!/bin/bash
set -euo pipefail

echo "--- Running Terraform module tests ---"

# Initialize Terraform in the test directory
echo "Initializing Terraform..."
# Mock rationale: -backend=false prevents Terraform from trying to configure a real backend,
# making the init process purely local and offline for module testing.
terraform -chdir=tests init -backend=false

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
# Mock rationale: terraform validate performs static analysis of the configuration
# and does not require AWS credentials or live API calls.
terraform -chdir=tests validate

# Generate a destroy plan (offline check for resource teardown)
echo "Generating Terraform destroy plan..."
# Mock rationale: terraform plan -destroy generates a plan to destroy resources.
# When run with mock credentials and -input=false -no-color, it performs a dry-run
# without interacting with the AWS API, ensuring the configuration is valid for teardown.
# The existence of the tfplan file and a successful exit code confirm the module's integrity.
terraform -chdir=tests plan -destroy -out=tests/tfplan -input=false -no-color

# Check if the plan file was created successfully
if [ ! -f "tests/tfplan" ]; then
  echo "Error: Terraform destroy plan file was not created."
  exit 1
fi

echo "Terraform destroy plan generated successfully."

# Clean up the generated plan file
echo "Cleaning up generated plan file..."
rm tests/tfplan

echo "--- All Terraform tests passed! ---"
