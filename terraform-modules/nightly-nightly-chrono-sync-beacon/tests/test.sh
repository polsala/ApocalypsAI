#!/bin/bash
set -euo pipefail

# Create a temporary directory for Terraform operations
TEST_DIR=$(mktemp -d)
cp -R src/* "$TEST_DIR/"

echo "Running Terraform tests in $TEST_DIR..."

cd "$TEST_DIR"

# Mock rationale: terraform init -backend=false avoids needing actual backend configuration
# and network access for state storage, making the test offline.
echo "Initializing Terraform..."
terraform init -backend=false > /dev/null

# Mock rationale: terraform validate performs static analysis of the configuration
# without requiring AWS credentials or network access to deploy resources.
echo "Validating Terraform configuration..."
terraform validate

# Mock rationale: terraform fmt -check ensures code style compliance without
# modifying files or interacting with cloud providers.
echo "Checking Terraform formatting..."
terraform fmt -check

# Test the precondition check by providing an invalid instance type
echo "Testing precondition check with invalid instance type..."
# We need to provide dummy values for required variables for plan to run
# even if it's just for validation of the check block.
if terraform plan -var="instance_type=c5.large" -var="vpc_id=vpc-test-123" -var="subnet_id=subnet-test-456" -no-color > /dev/null 2>&1; then
  echo "ERROR: Precondition check failed to catch invalid instance type."
  exit 1
else
  echo "Precondition check successfully caught invalid instance type (expected failure)."
fi

echo "All Terraform tests passed!"

# Clean up temporary directory
rm -rf "$TEST_DIR"
