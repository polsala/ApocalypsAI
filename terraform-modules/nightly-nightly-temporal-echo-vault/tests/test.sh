#!/bin/bash

set -euo pipefail

# Mock rationale: This test script performs static analysis and uses `terraform validate`
# and `terraform fmt -check` which are offline operations. It avoids `terraform plan`
# or `terraform apply` to ensure determinism and no cloud interaction.
# The checks for specific strings in .tf files act as a mock for verifying the
# intended configuration without actual execution.

echo "--- Running Terraform module tests ---"

# Ensure terraform is available
if ! command -v terraform &> /dev/null
then
    echo "Terraform CLI not found. Please install Terraform to run tests."
    exit 1
fi

# Go to the test directory
cd "$(dirname "$0")"

# Initialize Terraform in the test directory
echo "Initializing Terraform..."
# Mock rationale: terraform init creates local state and downloads providers.
# For offline testing, we only need the local state for `validate`.
# We'll use -backend=false to avoid needing a remote backend config.
# -input=false to prevent interactive prompts.
terraform init -backend=false -input=false > /dev/null
if [ $? -ne 0 ]; then
    echo "Terraform init failed."
    exit 1
fi
echo "Terraform init successful."

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate
if [ $? -ne 0 ]; then
    echo "Terraform validation failed."
    exit 1
fi
echo "Terraform validation successful."

# Check Terraform formatting
echo "Checking Terraform formatting..."
terraform fmt -check ../src/main.tf ../src/variables.tf ../src/outputs.tf main.tf
if [ $? -ne 0 ]; then
    echo "Terraform formatting check failed. Run 'terraform fmt' to fix."
    exit 1
fi
echo "Terraform formatting check successful."

# --- Static analysis to mock plan verification ---
# Mock rationale: Instead of running `terraform plan` which requires provider setup
# and potentially network access, we perform static checks on the HCL files
# to ensure the module is configured as expected. This verifies the *intent*
# of the module's configuration without actual cloud interaction.

echo "Performing static analysis for configuration verification (mocking plan)..."

# Check for aws_s3_bucket_versioning resource and its status
if ! grep -q 'resource "aws_s3_bucket_versioning" "echo_vault_versioning"' ../src/main.tf || \
   ! grep -q 'status = var.enable_versioning ? "Enabled" : "Suspended"' ../src/main.tf; then
    echo "ERROR: Versioning configuration not found or incorrect in src/main.tf"
    exit 1
fi
echo "Versioning configuration check passed."

# Check for aws_s3_bucket_lifecycle_configuration resource and key rules
if ! grep -q 'resource "aws_s3_bucket_lifecycle_configuration" "echo_vault_lifecycle"' ../src/main.tf; then
    echo "ERROR: Lifecycle configuration resource not found in src/main.tf"
    exit 1
fi

if ! grep -q 'id     = "current-version-intelligent-tiering"' ../src/main.tf || \
   ! grep -q 'storage_class = "INTELLIGENT_TIERING"' ../src/main.tf || \
   ! grep -q 'days          = var.echo_chamber_retention_days' ../src/main.tf; then
    echo "ERROR: Intelligent-Tiering transition rule not found or incorrect in src/main.tf"
    exit 1
fi
echo "Intelligent-Tiering transition rule check passed."

if ! grep -q 'id     = "non-current-version-glacier-transition"' ../src/main.tf || \
   ! grep -q 'storage_class = "GLACIER"' ../src/main.tf || \
   ! grep -q 'days          = var.echo_chamber_glacier_days' ../src/main.tf; then
    echo "ERROR: Glacier transition rule for non-current versions not found or incorrect in src/main.tf"
    exit 1
fi
echo "Glacier transition rule check passed."

if ! grep -q 'id     = "non-current-version-decay"' ../src/main.tf || \
   ! grep -q 'noncurrent_version_expiration' ../src/main.tf || \
   ! grep -q 'days = var.echo_chamber_decay_days' ../src/main.tf; then
    echo "ERROR: Non-current version decay rule not found or incorrect in src/main.tf"
    exit 1
fi
echo "Non-current version decay rule check passed."

echo "All static analysis checks passed."

echo "--- All Terraform module tests passed successfully! ---"

# Clean up .terraform directory
echo "Cleaning up .terraform directory..."
rm -rf .terraform .terraform.lock.hcl
echo "Cleanup complete."
