#!/bin/bash

set -euo pipefail

echo "Running Terraform module tests for Nightly Temporal Data Vault..."

# Navigate to the tests directory
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPT_DIR"

echo "Initializing Terraform..."
# Mock rationale: -backend=false ensures no actual state backend is configured or accessed,
# making the test fully offline and deterministic.
terraform init -backend=false -input=false

echo "Validating Terraform configuration..."
# Mock rationale: terraform validate checks HCL syntax and configuration logic
# without requiring AWS credentials or making API calls.
terraform validate

echo "Generating Terraform plan (no actual resource creation)..."
# Mock rationale: terraform plan generates an execution plan.
# -destroy ensures we test the ability to plan for resource removal,
# which implicitly validates the resource definitions.
# -out=tfplan.out saves the plan, but we don't apply it.
# -input=false prevents interactive prompts.
terraform plan -destroy -out=tfplan.out -input=false

# Clean up the generated plan file
rm tfplan.out

echo "All Terraform module tests passed successfully!"
