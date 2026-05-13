#!/bin/bash
set -euo pipefail

echo "Running Terraform validation and formatting checks for the module..."

# Change to the test directory
cd "$(dirname "$0")"

# Initialize Terraform (downloads providers, but doesn't authenticate)
# Mock rationale: `terraform init` is required to download provider plugins
# and parse module dependencies, but no actual cloud resources are touched.
# The `-backend=false` flag ensures no remote state operations.
terraform init -backend=false

# Validate the Terraform configuration
echo "Running terraform validate..."
terraform validate

# Check formatting
echo "Running terraform fmt --check..."
terraform fmt --check

echo "All Terraform checks passed!"
