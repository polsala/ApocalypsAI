#!/bin/bash
set -euo pipefail

echo "-- Running Terraform module tests --"

# Mock rationale: These tests are offline and deterministic.
# They validate the HCL syntax and formatting without requiring AWS credentials
# or actual resource provisioning. They ensure the module is syntactically correct
# and adheres to formatting standards.

# Initialize Terraform in a temporary directory without a backend
# -chdir=src ensures commands run in the module's source directory
echo "Initializing Terraform..."
terraform -chdir=src init -backend=false

# Validate the Terraform configuration for syntax and internal consistency
echo "Validating Terraform configuration..."
terraform -chdir=src validate

# Check Terraform formatting. Exits with non-zero if files are not formatted.
# -check: Check if the input is formatted
# -diff: Display diffs of non-conforming files
echo "Checking Terraform formatting..."
terraform -chdir=src fmt -check -diff

echo "All Terraform module tests passed successfully!"
