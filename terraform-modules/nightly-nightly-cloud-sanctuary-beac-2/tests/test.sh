#!/bin/bash
set -euo pipefail

echo "--- Running Terraform module tests ---"

# Initialize Terraform in the test directory
echo "Initializing Terraform..."
terraform init -backend=false # Mock rationale: Prevents Terraform from trying to connect to a real backend, making the test offline.
if [ $? -ne 0 ]; then
  echo "Terraform init failed!"
  exit 1
fi
echo "Terraform init successful."

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate
if [ $? -ne 0 ]; then
  echo "Terraform validation failed!"
  exit 1
fi
echo "Terraform validation successful."

# Plan the Terraform configuration and check for changes
# -detailed-exitcode: 0 = no changes, 1 = error, 2 = changes
echo "Planning Terraform configuration (expecting changes)..."
terraform plan -detailed-exitcode -out=tfplan.out
PLAN_EXIT_CODE=$?

if [ $PLAN_EXIT_CODE -eq 0 ]; then
  echo "Terraform plan showed no changes, but new resources are expected. Test failed!"
  rm -f tfplan.out
  exit 1
elif [ $PLAN_EXIT_CODE -eq 1 ]; then
  echo "Terraform plan failed!"
  rm -f tfplan.out
  exit 1
elif [ $PLAN_EXIT_CODE -eq 2 ]; then
  echo "Terraform plan successful (changes detected, as expected for new resources)."
  rm -f tfplan.out
  echo "--- All Terraform module tests passed! ---"
  exit 0
else
  echo "Unexpected exit code from terraform plan: $PLAN_EXIT_CODE. Test failed!"
  rm -f tfplan.out
  exit 1
fi
