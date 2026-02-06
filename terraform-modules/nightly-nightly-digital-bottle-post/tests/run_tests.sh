#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests..."

# Initialize Terraform in the test directory
echo "Initializing Terraform..."
terraform -chdir=tests init -backend=false

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform -chdir=tests validate

# Plan the Terraform configuration (without applying)
# This checks for syntax errors, variable issues, and provider configuration.
# Mock rationale: We are generating plan files for the configurations defined in test_module.tf.
# This is an offline check of the module's behavior under different input conditions.

echo "Planning Terraform configuration for public bucket test..."
terraform -chdir=tests plan -target=module.digital_bottle_post_public_test -out=tfplan_public -no-color

echo "Planning Terraform configuration for private bucket test..."
terraform -chdir=tests plan -target=module.digital_bottle_post_private_test -out=tfplan_private -no-color

# Basic check for resource creation in the plan output (offline check)
# Mock rationale: We're parsing the plan output to ensure expected resources are present
# and conditional logic (public access block) is correctly applied.
# This is a mock of actual resource creation validation, relying on textual output.

# Check public bucket plan
if grep -q "aws_s3_bucket.message_bottle" tfplan_public && \
   grep -q "aws_s3_bucket_object.initial_message" tfplan_public && \
   ! grep -q "aws_s3_bucket_public_access_block.message_bottle_access_block" tfplan_public; then
  echo "Public bucket plan check passed: Expected resources found, public access block NOT found."
else
  echo "Public bucket plan check failed: Expected resources not found or public access block found unexpectedly."
  exit 1
fi

# Check private bucket plan
if grep -q "aws_s3_bucket.message_bottle" tfplan_private && \
   grep -q "aws_s3_bucket_object.initial_message" tfplan_private && \
   grep -q "aws_s3_bucket_public_access_block.message_bottle_access_block" tfplan_private; then
  echo "Private bucket plan check passed: Expected resources found, public access block found."
else
  echo "Private bucket plan check failed: Expected resources not found or public access block missing."
  exit 1
fi

echo "All Terraform module tests passed successfully."

# Clean up generated plan files
rm -f tfplan_public tfplan_private
