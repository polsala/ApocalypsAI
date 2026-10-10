#!/bin/bash
set -euo pipefail

echo "--- Running Terraform module tests ---"

# Navigate to the test directory
cd "$(dirname "$0")"

# Initialize Terraform in the test directory without a backend
# Mock rationale: -backend=false ensures no remote state interaction, making the test offline.
echo "Initializing Terraform (offline)..."
terraform init -backend=false

# Validate the Terraform configuration
# Mock rationale: terraform validate checks syntax and configuration logic without cloud interaction.
echo "Validating Terraform configuration..."
terraform validate

# Plan a destroy operation to ensure all resources can be correctly planned for destruction
# This checks the module's ability to generate a valid plan, including conditional resources.
# Mock rationale: terraform plan -destroy is an offline dry-run that verifies the resource graph
# and configuration without provisioning actual cloud resources. It's deterministic.
echo "Planning a destroy operation (offline dry-run)..."
terraform plan -destroy -out=tfdestroy.plan

echo "Terraform module tests passed successfully!"

# Clean up generated plan file
rm tfdestroy.plan
