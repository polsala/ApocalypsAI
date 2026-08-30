#!/bin/bash

# Mock rationale: This script provides a deterministic, offline test by
# validating the Terraform module's syntax and plan generation without
# interacting with actual cloud infrastructure. 'terraform init' and
# 'terraform plan' are run in a controlled environment.

set -e # Exit immediately if a command exits with a non-zero status

echo "--- Running Terraform module tests ---"

# Navigate to the test directory
cd "$(dirname "$0")"

# Initialize Terraform in the test directory
echo "Initializing Terraform..."
terraform init -backend=false # -backend=false prevents state backend configuration, making it fully offline

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Generate a plan and check for errors
# -detailed-exitcode provides specific exit codes:
# 0 = Succeeded with no diffs (e.g., plan against existing state)
# 1 = Errored
# 2 = Succeeded with diffs (e.g., initial plan)
echo "Generating Terraform plan..."
terraform plan -out=tfplan -detailed-exitcode

PLAN_EXIT_CODE=$?

if [ $PLAN_EXIT_CODE -eq 0 ]; then
  echo "SUCCESS: Terraform plan generated with no changes (expected for initial plan against empty state, or if no changes are detected)."
elif [ $PLAN_EXIT_CODE -eq 2 ]; then
  echo "SUCCESS: Terraform plan generated with changes (expected for initial plan creating resources)."
else
  echo "FAILURE: Terraform plan failed with exit code $PLAN_EXIT_CODE."
  exit 1
fi

# Clean up generated plan file
rm -f tfplan

echo "--- All Terraform tests passed! ---"
