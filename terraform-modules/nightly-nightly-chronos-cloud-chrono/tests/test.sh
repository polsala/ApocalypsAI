#!/bin/bash
set -euo pipefail

echo "--- Running Terraform module tests ---"

# Change to the tests directory
cd "$(dirname "$0")"

# Initialize Terraform in offline mode
echo "Initializing Terraform (offline)..."
terraform init -backend=false

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Generate a Terraform plan and check for no changes
# Mock rationale: `terraform plan` simulates the deployment without touching real AWS resources.
# `-detailed-exitcode` returns 0 for no changes, 1 for error, 2 for changes.
# We expect 0 here, meaning the plan is stable and valid for the given inputs.
echo "Generating Terraform plan (expecting no changes)..."
if ! terraform plan -detailed-exitcode -out=tfplan; then
    PLAN_EXIT_CODE=$?
    if [ "$PLAN_EXIT_CODE" -eq 2 ]; then
        echo "Terraform plan detected changes. This might be expected for initial deployment, but for a stable test, we expect no changes."
        echo "Review the plan output above for details."
        exit 1
    elif [ "$PLAN_EXIT_CODE" -eq 1 ]; then
        echo "Terraform plan failed with an error."
        exit 1
    else
        echo "Terraform plan succeeded with unexpected exit code: $PLAN_EXIT_CODE"
        exit 1
    fi
else
    echo "Terraform plan successful. No changes detected (exit code 0)."
fi

# Clean up the plan file
rm tfplan

echo "--- All Terraform module tests passed! ---"
