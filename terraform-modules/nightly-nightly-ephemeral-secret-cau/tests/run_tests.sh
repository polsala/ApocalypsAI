#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests..."

TEST_DIR="tests"
MODULE_DIR="src"

# Check if the module directory exists
if [ ! -d "$MODULE_DIR" ]; then
  echo "Error: Module source directory '$MODULE_DIR' not found."
  exit 1
fi

# Initialize Terraform in the test directory
echo "Initializing Terraform in $TEST_DIR..."
terraform -chdir="$TEST_DIR" init -backend=false -upgrade

# Validate the Terraform configuration
echo "Validating Terraform configuration in $TEST_DIR..."
terraform -chdir="$TEST_DIR" validate

# Plan a destroy operation to ensure resources are correctly defined for destruction
# Mock rationale: This command simulates a destroy plan without requiring actual AWS credentials.
# It verifies that the module's resources can be targeted for destruction,
# ensuring structural integrity for lifecycle management.
echo "Planning destroy operation in $TEST_DIR (mocked)..."
terraform -chdir="$TEST_DIR" plan -destroy -out=/dev/null -var="secret_name=mock-secret" -var="secret_string=mock-value"

echo "All Terraform module tests passed successfully!"
