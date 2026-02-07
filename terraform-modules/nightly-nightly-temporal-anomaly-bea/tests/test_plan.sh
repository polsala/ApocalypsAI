#!/bin/bash
set -euo pipefail

echo "Running Terraform module validation and plan test..."

# Change to the test directory
cd "$(dirname "$0")"

# Initialize Terraform (downloads providers, etc.)
# Mock rationale: 'terraform init' downloads provider plugins locally.
# It does not require AWS credentials for this step, only for actual resource provisioning.
# The -backend=false flag ensures no remote state is configured.
terraform init -backend=false

# Validate the Terraform configuration
terraform validate

# Plan the Terraform configuration without applying
# Mock rationale: 'terraform plan' performs a dry run, checking syntax and logic
# against the provider schema without making actual API calls to AWS.
# The -no-color flag makes output easier to parse programmatically.
terraform plan -out=tfplan -no-color

# Check if the plan indicates resources to be added
if grep -q "Plan: 1 to add, 0 to change, 0 to destroy." tfplan; then
  echo "Terraform plan successful and indicates 1 resource to add."
  exit 0
else
  echo "Terraform plan did not indicate the expected resource changes."
  cat tfplan
  exit 1
fi
