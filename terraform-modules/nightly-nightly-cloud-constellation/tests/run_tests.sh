#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests..."

# Change to the test directory
cd "$(dirname "$0")"

echo "Initializing Terraform..."
# Mock rationale: Disable backend and plugin download for offline test.
# This ensures the test runs without external network calls for providers or state.
terraform init -backend=false -get-plugins=false

echo "Validating Terraform configuration syntax..."
terraform validate

echo "Checking Terraform formatting..."
terraform fmt -check

# Mock rationale: This is a basic check for the module's planability and output declaration.
# It does not provision resources or require live AWS credentials beyond what 'validate' needs.
# The '-out=/dev/null' suppresses detailed plan output.
echo "Checking if module outputs are declared and accessible via plan..."
if ! terraform plan -target=module.test_celestial_bucket -out=/dev/null > /dev/null 2>&1; then
  echo "Error: Terraform plan failed, module outputs might not be accessible or configuration is invalid."
  exit 1
fi

echo "All Terraform module tests passed!"
