#!/bin/bash
set -euo pipefail

echo "--- Running Terraform module tests ---"

# Navigate to the test directory
cd "$(dirname "$0")"

# Initialize Terraform (downloads providers, etc.)
# Mock rationale: -backend=false prevents state file operations, making it offline.
# -input=false avoids interactive prompts.
echo "Initializing Terraform..."
terraform init -backend=false -input=false

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Plan the Terraform configuration (without applying)
# Mock rationale: -out=tfplan creates a plan file but doesn't apply it.
# -detailed-exitcode provides specific exit codes for changes/no changes.
echo "Generating Terraform plan..."
terraform plan -out=tfplan -detailed-exitcode -input=false

# Check the exit code of terraform plan
# 0 = Succeeded with no changes
# 1 = Errored
# 2 = Succeeded with changes
PLAN_EXIT_CODE=$?

if [ "$PLAN_EXIT_CODE" -eq 0 ]; then
  echo "Terraform plan succeeded with no changes (expected for a fresh plan)."
elif [ "$PLAN_EXIT_CODE" -eq 2 ]; then
  echo "Terraform plan succeeded with changes (expected for a fresh plan)."
else
  echo "Terraform plan failed with exit code $PLAN_EXIT_CODE."
  exit 1
fi

# Clean up the plan file
rm tfplan

echo "--- All Terraform tests passed! ---"
