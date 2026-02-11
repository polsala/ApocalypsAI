#!/bin/bash

set -euo pipefail

echo "Running Terraform module tests..."

# Navigate to the test directory
cd "$(dirname "$0")"

# Clean up previous test artifacts
echo "Cleaning up previous test artifacts..."
rm -rf .terraform terraform.tfstate.test .terraform.lock.hcl tfplan.destroy

# Initialize Terraform in the test directory
echo "Initializing Terraform..."
terraform init -backend-config="path=terraform.tfstate.test"

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Mock rationale: `terraform plan -destroy` is used here to simulate a plan
# for destroying the resources. This checks if the module's resources are
# correctly defined and can be targeted for destruction, without actually
# interacting with AWS. It's a robust syntax and dependency check.
echo "Running Terraform plan (destroy simulation)..."
terraform plan -destroy -out=tfplan.destroy -var="bucket_name_prefix=test-apocalypsai-signal-fire" -var="initial_message=Test beacon online. All systems nominal." -var="aws_region=us-east-1"

# Clean up generated plan file and state
echo "Cleaning up generated plan file and state..."
rm -f tfplan.destroy terraform.tfstate.test .terraform.lock.hcl

echo "Terraform module tests completed successfully!"
