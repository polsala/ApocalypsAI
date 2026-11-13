#!/bin/bash
set -e

echo "Running Terraform module tests for nightly-ephemeral-message-beacon..."

# Ensure Terraform is installed
if ! command -v terraform &> /dev/null
then
    echo "Terraform could not be found. Please install it to run tests."
    exit 1
fi

# Change to the test directory
TEST_DIR="$(dirname "$0")"
cd "$TEST_DIR"

# Initialize Terraform (downloads providers, etc.)
echo "Initializing Terraform..."
# Mock rationale: -backend=false prevents Terraform from trying to connect to a real state backend,
# making the test fully offline and deterministic for plan generation.
terraform init -backend=false

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Generate a plan and check for expected changes
echo "Generating Terraform plan..."
# -detailed-exitcode: 0=no changes, 1=error, 2=changes
# We expect '2' because we are planning to create new resources.
terraform plan -detailed-exitcode -out=tfplan

PLAN_EXIT_CODE=$?

if [ $PLAN_EXIT_CODE -eq 2 ]; then
  echo "Terraform plan generated successfully with expected changes (exit code 2)."
  # Optionally, inspect the plan output for specific resource creation
  # terraform show -json tfplan | jq '.resource_changes[] | select(.type=="aws_s3_bucket") | .change.actions[]' | grep -q 'create'
  # For this simple test, just checking the exit code is sufficient for module validity.
else
  echo "Terraform plan failed or did not propose expected changes (exit code $PLAN_EXIT_CODE)."
  exit 1
fi

echo "All tests passed for nightly-ephemeral-message-beacon!"
