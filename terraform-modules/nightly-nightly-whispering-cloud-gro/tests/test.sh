#!/bin/bash

# Mock rationale: This script performs offline validation and planning
# without interacting with actual AWS infrastructure.
# It uses `terraform validate` for syntax checks and `terraform plan -destroy`
# to ensure a plan can be generated, which implicitly checks resource definitions
# and variable usage.

set -euo pipefail

echo "--- Running Terraform tests for nightly-whispering-cloud-grove ---"

# Ensure terraform is installed
if ! command -v terraform &> /dev/null
then
    echo "Terraform could not be found. Please install Terraform to run tests."
    exit 1
fi

# Initialize Terraform in the test directory
echo "Initializing Terraform..."
terraform init -backend=false # Mock rationale: -backend=false prevents state file operations, making it offline.

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Generate a plan to ensure all resources and variables are correctly defined
# Using -destroy to ensure it can plan for cleanup, which covers resource definitions.
echo "Generating a Terraform plan (destroy)..."
terraform plan -destroy -out=tfplan.out

# Clean up the generated plan file
rm tfplan.out

echo "Terraform tests passed successfully!"
