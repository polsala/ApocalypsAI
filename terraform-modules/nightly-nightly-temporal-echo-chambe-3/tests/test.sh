#!/bin/bash
set -euo pipefail

# Mock rationale: This test script performs an offline 'terraform plan'
# and inspects its JSON output. It does not interact with AWS APIs,
# ensuring determinism and independence from cloud credentials.
# 'jq' is used to parse the JSON plan for assertions.

echo "--- Running Terraform module tests ---"

# Initialize Terraform in the test directory
echo "Initializing Terraform..."
terraform -chdir=tests init -backend=false > /dev/null

# Generate a plan file
echo "Generating Terraform plan..."
terraform -chdir=tests plan -out=tests/tfplan -no-color > /dev/null

# Convert the plan to JSON for inspection
echo "Converting plan to JSON..."
terraform -chdir=tests show -json tests/tfplan > tests/tfplan.json

# Assertions using jq
echo "Performing assertions..."

# 1. Check if aws_s3_bucket resource is planned
if ! jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.actions[] == "create")' tests/tfplan.json > /dev/null; then
  echo "Test Failed: aws_s3_bucket resource not found in plan."
  exit 1
fi
echo "  ✓ aws_s3_bucket resource found."

# 2. Check if aws_s3_bucket_public_access_block is planned and configured
if ! jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_public_access_block" and .change.actions[] == "create") | .change.after | select(.block_public_acls == false and .ignore_public_acls == false and .block_public_policy == false and .restrict_public_buckets == false)' tests/tfplan.json > /dev/null; then
  echo "Test Failed: aws_s3_bucket_public_access_block not configured as expected (allowing public access)."
  exit 1
fi
echo "  ✓ aws_s3_bucket_public_access_block configured to allow public access."

# 3. Check if aws_s3_bucket_lifecycle_configuration is planned and has an expiration rule
if ! jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_lifecycle_configuration" and .change.actions[] == "create") | .change.after.rule[] | select(.id == "expire-old-echoes" and .status == "Enabled" and .expiration.days == 14)' tests/tfplan.json > /dev/null; then
  echo "Test Failed: aws_s3_bucket_lifecycle_configuration with 'expire-old-echoes' rule and 14 days not found."
  exit 1
fi
echo "  ✓ aws_s3_bucket_lifecycle_configuration with expiration rule found."

# 4. Check for expected outputs
if ! jq -e '.outputs.test_bucket_id.value' tests/tfplan.json > /dev/null; then
  echo "Test Failed: Output 'test_bucket_id' not found."
  exit 1
fi
if ! jq -e '.outputs.test_bucket_arn.value' tests/tfplan.json > /dev/null; then
  echo "Test Failed: Output 'test_bucket_arn' not found."
  exit 1
}
if ! jq -e '.outputs.test_bucket_regional_domain_name.value' tests/tfplan.json > /dev/null; then
  echo "Test Failed: Output 'test_bucket_regional_domain_name' not found."
  exit 1
fi
echo "  ✓ All expected outputs found."

echo "--- All Terraform module tests passed! ---"

# Clean up generated files
rm tests/tfplan tests/tfplan.json
