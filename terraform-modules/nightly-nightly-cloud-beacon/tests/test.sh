#!/bin/bash
set -euo pipefail

# Mock rationale: This test validates the Terraform module's syntax and plan generation
# without actually deploying resources to AWS. It ensures the module is well-formed
# and its outputs are correctly defined in the outputs.tf file. This is a deterministic
# and offline test as it does not interact with any live cloud resources.

echo "--- Running Terraform module tests ---"

# Navigate to the test directory
cd "$(dirname "$0")"

# Ensure terraform is available
if ! command -v terraform &> /dev/null
then
    echo "Error: terraform command not found. Please install Terraform to run these tests."
    exit 1
fi

# Initialize Terraform in the test configuration
echo "Initializing Terraform..."
# -backend=false prevents Terraform from trying to configure a state backend (e.g., S3, remote)
# -input=false prevents Terraform from prompting for input variables
terraform init -backend=false -input=false

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Generate a Terraform plan to ensure it's syntactically correct and can form a plan
# -detailed-exitcode will exit with 2 if there are changes (which we expect for a new deployment)
# or 0 if no changes (not expected here), or 1 if error.
echo "Generating Terraform plan (expecting changes for a new deployment)..."
terraform plan -detailed-exitcode -out=tfplan

# Check the exit code of terraform plan
PLAN_EXIT_CODE=$?
if [ "$PLAN_EXIT_CODE" -eq 0 ]; then
    echo "Terraform plan showed no changes. This is acceptable for a module test if resources are already defined, but for a fresh test, changes are typically expected."
elif [ "$PLAN_EXIT_CODE" -eq 2 ]; then
    echo "Terraform plan showed pending changes (expected for a new deployment)."
else
    echo "Terraform plan failed with exit code $PLAN_EXIT_CODE."
    exit 1
fi

# Verify that the expected outputs are defined in the module's outputs.tf
echo "Verifying expected outputs are defined in src/outputs.tf..."
OUTPUTS_FILE="../src/outputs.tf"
if ! grep -q 'output "s3_bucket_id"' "$OUTPUTS_FILE"; then
    echo "Error: Output 's3_bucket_id' not found in $OUTPUTS_FILE."
    exit 1
fi
if ! grep -q 'output "cloudfront_domain_name"' "$OUTPUTS_FILE"; then
    echo "Error: Output 'cloudfront_domain_name' not found in $OUTPUTS_FILE."
    exit 1
fi
if ! grep -q 'output "cloudfront_distribution_id"' "$OUTPUTS_FILE"; then
    echo "Error: Output 'cloudfront_distribution_id' not found in $OUTPUTS_FILE."
    exit 1
fi

echo "All Terraform module tests passed successfully!"
rm -f tfplan # Clean up the plan file
exit 0
