#!/bin/bash

set -euo pipefail

echo "Running Terraform module tests..."

# Navigate to the test configuration directory
SCRIPT_DIR=$(dirname "$(realpath "$0")")
cd "$SCRIPT_DIR"

# Initialize Terraform
echo "Initializing Terraform..."
# Mock rationale: terraform init downloads providers, but does not interact with cloud APIs
# when only validating or planning. It's a prerequisite for `validate` and `plan`.
# The -backend=false flag ensures no remote state backend is configured, making it truly offline.
terraform init -backend=false > /dev/null

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
if ! terraform validate; then
  echo "Terraform validation failed!"
  exit 1
fi
echo "Terraform validation passed."

# Plan the Terraform configuration and check for errors
echo "Planning Terraform configuration..."
# Mock rationale: terraform plan generates an execution plan locally without applying it.
# It checks for syntax errors, logical inconsistencies, and provider configuration issues.
# We pipe stderr to stdout to capture potential errors from plan.
if ! terraform plan -no-color -out=tfplan.out > /dev/null; then
  echo "Terraform plan failed!"
  exit 1
fi
echo "Terraform plan passed."

# Clean up generated plan file
rm -f tfplan.out

echo "All Terraform module tests passed successfully!"
