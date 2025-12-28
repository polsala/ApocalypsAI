#!/bin/bash

set -e

# Change to the directory where the test configuration resides
cd "$(dirname "$0")"

echo "Starting Terraform module tests..."

# Initialize Terraform in the test directory without a backend
# Mock rationale: '-backend=false' ensures no state file is created or accessed,
# making the test fully offline and deterministic. It only checks configuration syntax.
echo "Initializing Terraform (offline mode)..."
terraform init -backend=false

# Validate the Terraform configuration
# Mock rationale: 'terraform validate' checks the syntax and internal consistency
# of the configuration, including variable definitions and resource references,
# without requiring actual cloud API calls or credentials.
echo "Validating Terraform configuration..."
terraform validate

echo "Terraform module tests passed successfully!"
