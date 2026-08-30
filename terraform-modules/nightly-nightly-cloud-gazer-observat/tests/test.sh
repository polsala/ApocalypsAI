#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests..."

# Change to the test directory
cd "$(dirname "$0")"

# Initialize Terraform in the test directory
echo "Initializing Terraform..."
terraform init -backend=false -input=false

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Plan the Terraform configuration (without applying)
# This checks for syntax errors, variable issues, and provider configuration.
# Mock rationale: `terraform plan` is run to ensure the module can be planned successfully
# without actual AWS credentials, relying on the mock provider configuration in `main.tf`.
# The output is discarded as we only care about the exit code.
echo "Planning Terraform configuration..."
terraform plan -out=tfplan -input=false -no-color

echo "Terraform module tests passed successfully!"

# Clean up the plan file
rm -f tfplan
