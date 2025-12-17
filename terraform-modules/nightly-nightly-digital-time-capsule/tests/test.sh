#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests..."

# Change to the tests directory
cd "$(dirname "$0")"

# Initialize Terraform
echo "Initializing Terraform..."
# Mock rationale: -backend=false prevents Terraform from configuring a real backend,
# ensuring the test is offline and does not interact with cloud state storage.
terraform init -backend=false
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

# Plan a destroy operation to ensure the configuration is valid for resource management.
# This checks if Terraform can parse and understand the resources defined and form a valid plan.
# Mock rationale: -destroy ensures no resources are created. -out=tfplan saves the plan
# locally without applying it, making the test offline and deterministic.
echo "Planning a destroy operation (offline check)..."
terraform plan -destroy -out=tfplan -var="bucket_name=apocalypsai-test-time-capsule-12345"
if [ $? -ne 0 ]; then
  echo "Terraform plan -destroy failed!"
  exit 1
fi
echo "Terraform plan -destroy successful. Plan saved to tfplan."

# Clean up the plan file
rm tfplan

echo "All Terraform module tests passed successfully!"
