#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests for nightly-ephemeral-vault..."

# Change to the tests directory
cd "$(dirname "$0")"

# Initialize Terraform in the test directory
# -backend=false prevents Terraform from trying to configure a backend,
# which is not needed for syntax validation and makes it truly offline.
echo "Initializing Terraform..."
terraform init -backend=false

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# If validate passes, the test is considered successful
echo "Terraform validation successful. Module syntax and variable usage are correct."

# Clean up .terraform directory
echo "Cleaning up .terraform directory..."
rm -rf .terraform .terraform.lock.hcl

echo "All tests passed for nightly-ephemeral-vault."
