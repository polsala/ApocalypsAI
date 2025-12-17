#!/bin/bash
set -euo pipefail

echo "--- Running Terraform module tests ---"

# Initialize Terraform in the test directory
echo "Initializing Terraform..."
terraform -chdir=tests init -backend=false # Mock rationale: -backend=false ensures no remote state backend is configured, making the test fully offline.

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform -chdir=tests validate

# Generate a plan to ensure syntax and variable usage are correct
# Use -destroy to ensure all resource definitions are valid for deletion too
echo "Generating a Terraform destroy plan (offline validation)..."
terraform -chdir=tests plan -destroy -out=tests/tfplan # Output to tests/tfplan to keep it contained

echo "Terraform module tests passed successfully!"

# Clean up generated plan file
rm -f tests/tfplan
