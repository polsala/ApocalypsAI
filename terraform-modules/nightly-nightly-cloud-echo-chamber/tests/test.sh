#!/bin/bash
set -euo pipefail

# Mock rationale: This test script performs an offline validation of the Terraform module
# without deploying any actual AWS resources. It uses `terraform validate` which only
# checks the syntax and configuration logic against the Terraform language specification
# and provider schemas, not against live cloud state. This ensures determinism and
# avoids incurring costs or requiring credentials. The `archive` provider is a local
# provider and its download during `terraform init` is deterministic and does not
# interact with AWS APIs.

echo "Running Nightly Cloud Echo Chamber Terraform module tests..."

# Create a temporary directory for testing
TEST_DIR=$(mktemp -d)
echo "Temporary test directory: $TEST_DIR"

# Copy the module source to the test directory
mkdir -p "$TEST_DIR/src/lambda"
cp -r ../src/* "$TEST_DIR/src/"
cp test_main.tf "$TEST_DIR/main.tf"

cd "$TEST_DIR"

# Initialize Terraform (backend=false for offline validation)
echo "Initializing Terraform..."
terraform init -backend=false

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Check if the validation was successful
if [ $? -eq 0 ]; then
    echo "Terraform validation successful!"
else
    echo "Terraform validation failed!"
    exit 1
fi

# Clean up the temporary directory
echo "Cleaning up temporary directory..."
rm -rf "$TEST_DIR"

echo "All tests passed for Nightly Cloud Echo Chamber."
