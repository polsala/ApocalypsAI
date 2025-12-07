#!/bin/bash

set -euo pipefail

echo "Running Terraform module tests for nightly-digital-data-bunker..."

# Create a temporary directory for testing
TEST_DIR=$(mktemp -d)
echo "Temporary test directory: $TEST_DIR"

# Mock rationale: Terraform validation is inherently offline and deterministic
# for syntax and configuration checks. We are not performing actual cloud deployments.
# The `terraform init -backend=false` command ensures no network calls for backend configuration.
# The `terraform validate` command checks the HCL syntax and configuration logic.
# The `provider "aws"` block in `test_bunker.tf` is a mock configuration for validation.

# Copy the module source into the temporary test directory
mkdir -p "$TEST_DIR/src"
cp src/*.tf "$TEST_DIR/src/"

# Copy the test configuration to the root of the temporary directory
cp tests/test_bunker.tf "$TEST_DIR/main.tf"

# Navigate to the temporary directory
pushd "$TEST_DIR" > /dev/null

# Initialize Terraform (without a backend to ensure offline operation)
echo "Initializing Terraform..."
terraform init -backend=false -input=false

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Check if validation was successful
if [ $? -eq 0 ]; then
  echo "Terraform validation successful!"
else
  echo "Terraform validation failed!"
  popd > /dev/null
  rm -rf "$TEST_DIR"
  exit 1
fi

# Clean up the temporary directory
popd > /dev/null
rm -rf "$TEST_DIR"

echo "All tests passed for nightly-digital-data-bunker."
