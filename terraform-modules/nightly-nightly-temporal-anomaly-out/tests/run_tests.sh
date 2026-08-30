#!/bin/bash
set -euo pipefail

echo "--- Running Terraform module tests ---"

# Change to the tests directory
SCRIPT_DIR=$(dirname "$(realpath "$0")")
cd "$SCRIPT_DIR"

echo "Initializing Terraform..."
# Mock rationale: -backend=false prevents Terraform from trying to configure a state backend,
# which is not needed for local module validation and plan generation.
terraform init -backend=false

echo "Validating Terraform configuration..."
terraform validate

echo "Generating Terraform plan..."
# Mock rationale: -out=tfplan saves the plan to a file, which can be inspected.
# We expect a successful plan generation, not necessarily a plan with no changes.
# -detailed-exitcode returns 0 for no changes, 1 for error, 2 for changes.
# For a fresh plan, we expect 2 (resources to be created).
terraform plan -out=tfplan -detailed-exitcode

PLAN_EXIT_CODE=$?

if [[ "$PLAN_EXIT_CODE" -eq 0 ]]; then
  echo "Terraform plan indicates no changes (this might happen if resources were already planned/applied in a previous run, or if the module is empty)."
  echo "Test passed: Terraform plan generated successfully with exit code 0."
elif [[ "$PLAN_EXIT_CODE" -eq 2 ]]; then
  echo "Terraform plan indicates changes to be applied (expected for a fresh module plan)."
  echo "Test passed: Terraform plan generated successfully with exit code 2."
else
  echo "Test failed: Terraform plan failed with exit code $PLAN_EXIT_CODE."
  exit 1
fi

echo "--- All Terraform module tests passed successfully! ---"
