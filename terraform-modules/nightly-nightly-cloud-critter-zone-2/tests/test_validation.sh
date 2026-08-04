#!/bin/bash
set -euo pipefail

echo "Running Terraform validation tests..."

# Change to the test directory
cd "$(dirname "$0")"

# Initialize Terraform in the test module directory
echo "Initializing Terraform..."
terraform init -backend=false -input=false

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Plan a destroy to ensure it can be planned (offline check)
echo "Planning a destroy to ensure configuration is valid for destruction..."
terraform plan -destroy -out=tfdestroy.plan -input=false

echo "Terraform validation tests passed!"

# Clean up
rm -f tfdestroy.plan
rm -rf .terraform

# Mock rationale: This test is deterministic and offline.
# It uses 'terraform init -backend=false' to avoid connecting to a real backend,
# and 'terraform validate' and 'terraform plan -destroy' to check the syntax
# and logical consistency of the module without provisioning actual cloud resources.
# The plan -destroy command is used as a robust offline check that the module
# can be processed by Terraform's engine.
