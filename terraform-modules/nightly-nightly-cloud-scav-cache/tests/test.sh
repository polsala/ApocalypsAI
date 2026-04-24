#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests..."

# Navigate to the test directory
cd "$(dirname "$0")"

# Initialize Terraform (downloads providers, etc. but doesn't connect to AWS)
echo "Initializing Terraform..."
terraform init -backend=false # Mock rationale: -backend=false prevents state backend configuration, making it offline.

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Check formatting
echo "Checking Terraform formatting..."
terraform fmt -check -recursive

echo "Terraform module tests passed successfully!"
