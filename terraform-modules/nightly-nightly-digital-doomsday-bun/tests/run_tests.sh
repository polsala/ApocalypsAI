#!/bin/bash

set -euo pipefail

echo "--- Running Terraform tests for Digital Doomsday Bunker ---"

# Check if terraform is installed
if ! command -v terraform &> /dev/null
then
    echo "Terraform could not be found. Please install Terraform to run tests."
    exit 1
fi

# Ensure we are in the tests directory
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPT_DIR"

echo "1. Checking Terraform format..."
terraform fmt -check -recursive ../src/
if [ $? -ne 0 ]; then
    echo "Terraform format check failed. Run 'terraform fmt -recursive ../src/' to fix."
    exit 1
fi
echo "Terraform format check passed."

echo "2. Initializing Terraform (backend=false for offline validation)..."
# Mock rationale: -backend=false ensures no actual state backend is configured,
# making the init purely local and deterministic for provider plugin download/setup.
terraform init -backend=false
if [ $? -ne 0 ]; then
    echo "Terraform initialization failed."
    exit 1
fi
echo "Terraform initialization passed."

echo "3. Validating Terraform configuration..."
# Mock rationale: terraform validate performs static analysis of the configuration,
# checking syntax, variable definitions, and provider configurations without
# requiring actual AWS credentials or API calls. It's fully deterministic and offline.
terraform validate
if [ $? -ne 0 ]; then
    echo "Terraform validation failed."
    exit 1
fi
echo "Terraform validation passed."

echo "--- All Terraform tests passed! ---"
