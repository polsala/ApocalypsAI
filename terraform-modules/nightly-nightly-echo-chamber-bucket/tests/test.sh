#!/bin/bash

set -e # Exit immediately if a command exits with a non-zero status.

echo "--- Running Terraform module tests ---"

# Navigate to the directory containing the test configuration
cd "$(dirname "$0")"

echo "Initializing Terraform..."
terraform init -backend=false # Mock rationale: No backend needed for offline validation
echo "Terraform init successful."

echo "Validating Terraform configuration..."
terraform validate
echo "Terraform validation successful."

echo "Checking Terraform format..."
terraform fmt --check
echo "Terraform format check successful."

echo "All Terraform module tests passed!"
