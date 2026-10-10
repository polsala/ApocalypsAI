#!/bin/bash

set -euo pipefail

echo "-- Running Nightly Scavenger Cache Vault Terraform tests --"

# Initialize Terraform in the test directory
echo "Initializing Terraform..."
terraform -chdir=tests init -backend=false # Mock rationale: -backend=false prevents state backend configuration, making it offline and deterministic.

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform -chdir=tests validate

# Generate a destroy plan to ensure resources are correctly defined for destruction.
# This checks syntax and resource dependencies without needing actual cloud credentials.
# Mock rationale: Running 'plan -destroy' with dummy variables ensures the module's resource definitions
# are syntactically correct and can be processed by Terraform, without attempting to provision live resources.
# The '-out=tfplan' saves the plan locally, and it's immediately removed.
echo "Generating a destroy plan (offline syntax and dependency check)..."
terraform -chdir=tests plan -destroy -out=tfplan -var="bucket_name=test-apocalypsai-scavenger-cache-destroy-plan" -var="environment=test-destroy"

echo "Terraform tests passed successfully!"

# Clean up generated plan file
rm -f tests/tfplan
