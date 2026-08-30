#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests..."

# Ensure jq is installed for JSON parsing
if ! command -v jq &> /dev/null
then
    echo "jq could not be found. Please install jq to run these tests (e.g., sudo apt-get install jq or brew install jq)."
    exit 1
fi

# Initialize Terraform in the test directory
terraform -chdir=tests init -backend=false -input=false

# Run terraform plan and capture output
PLAN_OUTPUT=$(terraform -chdir=tests plan -no-color -input=false -out=tfplan)

# Check if the plan was successful
if [ $? -ne 0 ]; then
  echo "Terraform plan failed!"
  exit 1
fi

echo "Terraform plan successful. Analyzing output..."

# Show the plan in JSON format for easier parsing
PLAN_JSON=$(terraform -chdir=tests show -json tfplan)

# Mock rationale: We are parsing the output of `terraform show -json`
# to verify that the module correctly defines the S3 bucket and its
# lifecycle configuration. This is a deterministic, offline test.

# Assert S3 bucket resource is created
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.actions[] == "create")' > /dev/null; then
  echo "Test failed: aws_s3_bucket resource not found in plan."
  exit 1
fi
echo "  - Verified: aws_s3_bucket resource will be created."

# Assert S3 bucket lifecycle configuration resource is created
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_lifecycle_configuration" and .change.actions[] == "create")' > /dev/null; then
  echo "Test failed: aws_s3_bucket_lifecycle_configuration resource not found in plan.""
  exit 1
fi
echo "  - Verified: aws_s3_bucket_lifecycle_configuration resource will be created."

# Assert the expiration_days is set correctly in the lifecycle rule
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_lifecycle_configuration" and .change.after.rule[0].expiration[0].days == 3)' > /dev/null; then
  echo "Test failed: Lifecycle rule 'expiration.days' not set to 3."
  exit 1
fi
echo "  - Verified: Lifecycle rule 'expiration.days' is set to 3."

# Assert public access block is created and configured
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_public_access_block" and .change.after.block_public_acls == true and .change.after.block_public_and_cross_account_access == true)' > /dev/null; then
  echo "Test failed: aws_s3_bucket_public_access_block not configured correctly."
  exit 1
fi
echo "  - Verified: aws_s3_bucket_public_access_block configured."

# Clean up the plan file
rm tfplan

echo "All Terraform module tests passed!"
