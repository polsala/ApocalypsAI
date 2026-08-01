#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests..."

# Navigate to the tests directory
cd "$(dirname "$0")"

# Initialize Terraform in the test directory without a backend
# Mock rationale: This allows `terraform validate` and `terraform plan` to run offline
# without requiring actual AWS credentials or state storage.
echo "Initializing Terraform (backend disabled)..."
terraform init -backend=false

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Create a Terraform plan (dry run)
# Mock rationale: This checks if the configuration can be planned successfully,
# validating resource arguments against the provider schema without making actual API calls.
echo "Creating Terraform plan (dry run)..."
terraform plan -out=tfplan

# If all commands succeed, the test passes
echo "Terraform module tests passed successfully!"

# Clean up generated plan file
rm tfplan
