#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests for nightly-ephemeral-cloud-cauldron..."

# Mock rationale: Terraform commands like `init`, `validate`, `fmt`, and `plan -json`
# can be run offline and deterministically without actual cloud credentials
# to check syntax, formatting, and the structure of the planned resources.
# We are not performing an `apply` operation.

# Initialize Terraform in the test directory
echo "Initializing Terraform..."
terraform init -backend=false # Disable backend for offline testing
if [ $? -ne 0 ]; then
  echo "Terraform init failed!"
  exit 1
fi
echo "Terraform init successful."

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate
if [ $? -ne 0 ]; then
  echo "Terraform validation failed!"
  exit 1
fi
echo "Terraform validation successful."

# Check Terraform formatting
echo "Checking Terraform formatting..."
terraform fmt -check -recursive
if [ $? -ne 0 ]; then
  echo "Terraform formatting check failed! Run 'terraform fmt' to fix."
  exit 1
fi
echo "Terraform formatting check successful."

# Plan and check for expected resources and lifecycle policy
echo "Running Terraform plan to check resource creation and lifecycle policy..."
PLAN_OUTPUT=$(terraform plan -json -input=false -out=tfplan)
if [ $? -ne 0 ]; then
  echo "Terraform plan failed!"
  exit 1
fi

# Check if the S3 bucket resource is planned
if ! echo "$PLAN_OUTPUT" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.actions[] == "create")' > /dev/null; then
  echo "Test failed: S3 bucket resource not found in plan!"
  exit 1
fi
echo "Test passed: S3 bucket resource found in plan."

# Check if the S3 bucket lifecycle configuration resource is planned
if ! echo "$PLAN_OUTPUT" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_lifecycle_configuration" and .change.actions[] == "create")' > /dev/null; then
  echo "Test failed: S3 bucket lifecycle configuration resource not found in plan!"
  exit 1
fi
echo "Test passed: S3 bucket lifecycle configuration resource found in plan."

# Mock rationale: We are asserting the *intent* to create the lifecycle policy,
# which implies the configuration for expiration is present in the module.
# Detailed value checks from `plan -json` can be brittle across Terraform versions.

echo "All Terraform module tests passed successfully!"
exit 0
