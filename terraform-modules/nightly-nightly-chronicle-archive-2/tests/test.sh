#!/bin/bash

set -e

echo "Running Terraform module validation and plan generation tests..."

# Validate the source module itself
echo "\n--- Validating source module (src/) ---"
cd ../src
terraform init -backend=false # Initialize without backend for validation
terraform validate
cd -

# Validate the test configuration and generate a plan
echo "\n--- Validating test configuration (tests/) ---"
terraform init -backend=false # Initialize without backend for validation
terraform validate

echo "\n--- Generating Terraform plan (tests/) ---"
# Generate a plan without applying, using dummy variables for offline testing
# -out=tfplan saves the plan to a file
# -no-color for cleaner output in CI/CD logs
terraform plan -out=tfplan -var="bucket_name=test-chronicle-archive-$(date +%s)" -var="region=us-east-1" -no-color

echo "\nTerraform module validation and plan generation successful."

# Mock rationale: This test script performs static analysis (terraform validate) and plan generation (terraform plan)
# without applying any changes to actual cloud infrastructure. It verifies the HCL syntax, variable definitions,
# and the module's ability to generate a valid execution plan. The AWS provider is configured with dummy credentials
# in tests/main.tf to allow `terraform plan` to proceed without requiring live credentials, as no actual API calls
# are made during plan generation for resource creation. This ensures the tests are deterministic and offline.
