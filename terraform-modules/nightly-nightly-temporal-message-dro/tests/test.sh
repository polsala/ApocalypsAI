#!/bin/bash
set -euo pipefail

echo "--- Running Terraform module tests ---"

# Change to the tests directory
cd "$(dirname "$0")"

# Initialize Terraform
echo "Initializing Terraform..."
terraform init -backend=false # Mock rationale: -backend=false prevents state storage, making it offline.
if [ $? -ne 0 ]; then
  echo "Terraform init failed!"
  exit 1
fi
echo "Terraform init successful."

# Validate Terraform configuration
echo "Validating Terraform configuration..."
terraform validate
if [ $? -ne 0 ]; then
  echo "Terraform validation failed!"
  exit 1
fi
echo "Terraform validation successful."

# Plan Terraform changes (without applying)
echo "Planning Terraform changes..."
# Mock rationale: -out=test.tfplan saves the plan to a file without requiring actual cloud interaction.
# -detailed-exitcode provides specific exit codes for no changes, changes, or errors.
terraform plan -out=test.tfplan -detailed-exitcode
PLAN_EXIT_CODE=$?

if [ $PLAN_EXIT_CODE -eq 0 ]; then
  echo "Terraform plan successful: No changes detected (expected for a fresh plan)."
elif [ $PLAN_EXIT_CODE -eq 2 ]; then
  echo "Terraform plan successful: Changes detected (expected for a fresh plan)."
else
  echo "Terraform plan failed with exit code $PLAN_EXIT_CODE!"
  exit 1
fi

# Verify the plan contains the expected resource (e.g., an S3 bucket)
echo "Verifying plan output for expected resources..."
# Mock rationale: Grepping the plan output is an offline way to check for expected resource types.
if ! terraform show -json test.tfplan | grep -q "aws_s3_bucket.message_drop"; then
  echo "Error: aws_s3_bucket.message_drop not found in the plan!"
  exit 1
fi
echo "aws_s3_bucket.message_drop found in the plan."

echo "--- All Terraform module tests passed! ---"

# Clean up generated plan file
rm test.tfplan
