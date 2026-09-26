#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests..."

# Change to the test directory
cd "$(dirname "$0")"

# Initialize Terraform in the test directory
# -backend=false prevents Terraform from trying to configure a state backend,
# which is not needed for offline validation/plan.
echo "Initializing Terraform..."
terraform init -backend=false

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Generate a plan to ensure the configuration is deployable and destroyable
# -destroy ensures that a plan can be generated for resource destruction,
# which implies a valid creation plan.
# -out=plan.out saves the plan to a file, preventing interactive prompts.
echo "Generating Terraform plan (destroy simulation)..."
terraform plan -destroy -out=plan.out

# If all commands succeed, the test passes
echo "Terraform module tests passed successfully!"

# Clean up generated plan file
rm plan.out
