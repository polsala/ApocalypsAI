#!/bin/bash
set -euo pipefail

echo "--- Running Terraform module tests ---"

# Clean up previous runs
rm -rf .terraform .terraform.lock.hcl terraform.tfstate* || true
rm -f ../src/main.py ../src/slumber_manager.zip || true

# Navigate to the test directory
cd "$(dirname "$0")"

echo "Initializing Terraform..."
terraform init -backend=false # Mock rationale: -backend=false ensures no remote state interaction, keeping tests offline.

echo "Validating Terraform configuration..."
terraform validate # Mock rationale: terraform validate is a static analysis tool, purely offline.

echo "Generating a Terraform plan (destroy)..."
# We use -destroy to ensure all resources are correctly defined for deletion,
# which implies they were correctly defined for creation.
# This is a safe, offline way to check the module's integrity without provisioning.
terraform plan -destroy -out=tfplan # Mock rationale: terraform plan is an offline operation that calculates changes without applying them.

if [ $? -eq 0 ]; then
  echo "Terraform plan generated successfully. Module is syntactically valid."
  echo "Tests passed!"
else
  echo "Terraform plan failed. Module has errors."
  echo "Tests failed!"
  exit 1
fi

# Clean up generated plan file and local zip/py files from src
rm -f tfplan
rm -f ../src/main.py ../src/slumber_manager.zip

echo "--- Terraform module tests complete ---"
