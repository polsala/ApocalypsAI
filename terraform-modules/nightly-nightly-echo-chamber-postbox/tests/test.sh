#!/bin/bash

set -euo pipefail

echo "Running Nightly Echo Chamber Postbox Terraform module tests..."

# Initialize Terraform in the test directory
echo "Initializing Terraform..."
terraform init -backend=false # Mock rationale: Disable backend to ensure no remote state operations for offline test

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Plan a destroy operation to ensure the module can be planned without errors
# This checks syntax, variable resolution, and resource graph without provisioning anything.
echo "Planning a destroy operation (offline check)..."
terraform plan -destroy -out=tfplan.out

# Clean up the plan file
rm tfplan.out

echo "All Nightly Echo Chamber Postbox Terraform module tests passed successfully!"
