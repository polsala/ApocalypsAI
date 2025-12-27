#!/bin/bash
set -euo pipefail

echo "--- Running Terraform module tests ---"

# Navigate to the test configuration directory
cd "$(dirname "$0")"

# Initialize Terraform in the test configuration
echo "Initializing Terraform..."
# Mock rationale: -backend=false prevents Terraform from trying to connect to a real backend,
# making the init phase purely local and deterministic for module validation.
terraform init -backend=false

# Check Terraform formatting
echo "Checking Terraform formatting..."
# Mock rationale: terraform fmt -check -diff operates purely on local files,
# ensuring code style consistency without external dependencies.
terraform fmt -check -diff

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
# Mock rationale: terraform validate performs static analysis of the configuration,
# checking syntax, variable usage, and provider compatibility without requiring
# actual cloud credentials or API calls. It's fully offline and deterministic.
terraform validate

echo "All Terraform module tests passed successfully!"
