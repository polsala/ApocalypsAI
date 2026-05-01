#!/bin/bash
set -euo pipefail

echo "-- Running Terraform module tests --"

# Navigate to the test directory
cd "$(dirname "$0")"

# Initialize Terraform in the test directory
# -backend=false prevents Terraform from trying to configure a state backend,
# which is not needed for syntax validation and plan generation.
echo "Initializing Terraform..."
terraform init -backend=false

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Generate a Terraform plan
# -out=tfplan saves the plan to a file
# -detailed-exitcode provides specific exit codes:
#   0 = Succeeded, with no changes
#   1 = Errored
#   2 = Succeeded, with changes
echo "Generating Terraform plan (expecting exit code 0 or 2 for success)..."
terraform plan -out=tfplan -detailed-exitcode

PLAN_EXIT_CODE=$?

if [ "$PLAN_EXIT_CODE" -eq 0 ] || [ "$PLAN_EXIT_CODE" -eq 2 ]; then
  echo "Terraform plan generated successfully (exit code: $PLAN_EXIT_CODE)."
  rm tfplan # Clean up the plan file
else
  echo "Terraform plan failed (exit code: $PLAN_EXIT_CODE)."
  exit 1
fi

echo "-- All Terraform module tests passed! --"
