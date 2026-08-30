#!/bin/bash

set -euo pipefail

# Mock rationale: Set dummy AWS credentials to allow terraform init and plan
# to run without attempting to authenticate against a real AWS account.
# This ensures the tests are deterministic, offline, and do not incur costs.
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
export AWS_DEFAULT_REGION="us-east-1" # Required by the provider block in variables.tf

echo "--- Running Terraform module tests ---"

# Clean up previous runs
rm -rf .terraform .terraform.lock.hcl terraform.tfstate* tfplan*

echo "Initializing Terraform..."
terraform init -backend=false # -backend=false prevents state backend configuration, good for module tests
if [ $? -ne 0 ]; then
  echo "Terraform init failed!"
  exit 1
fi
echo "Terraform init successful."

echo "Validating Terraform configuration..."
terraform validate
if [ $? -ne 0 ]; then
  echo "Terraform validate failed!"
  exit 1
fi
echo "Terraform validate successful."

echo "Generating Terraform plan..."
# Use -input=false to avoid interactive prompts
# Use -detailed-exitcode to get specific exit codes for changes (0=no changes, 1=error, 2=changes)
# We expect changes (creation of resources), so exit code 2 is acceptable.
terraform plan -out=tfplan -input=false -detailed-exitcode
PLAN_EXIT_CODE=$?

if [ $PLAN_EXIT_CODE -eq 1 ]; then
  echo "Terraform plan failed with an error!"
  exit 1
elif [ $PLAN_EXIT_CODE -eq 0 ]; then
  echo "Terraform plan showed no changes (unexpected for initial creation)!"
  # This might indicate an issue if we expect resources to be created.
  # For a module test, we expect it to plan to create resources.
  echo "Expected plan to show resource creation, but it showed no changes."
  exit 1
elif [ $PLAN_EXIT_CODE -eq 2 ]; then
  echo "Terraform plan successful (changes detected, as expected)."
else
  echo "Terraform plan exited with unexpected code: $PLAN_EXIT_CODE"
  exit 1
fi

# Optional: Inspect the plan to ensure it contains expected resources
echo "Inspecting Terraform plan for expected resources..."
if ! terraform show -json tfplan | grep -q "aws_s3_bucket.chrono_cache"; then
  echo "Error: aws_s3_bucket.chrono_cache not found in plan!"
  exit 1
fi
echo "aws_s3_bucket.chrono_cache found in plan."

echo "--- All Terraform module tests passed! ---"

# Clean up generated files
echo "Cleaning up Terraform generated files..."
rm -rf .terraform .terraform.lock.hcl tfplan*
