#!/bin/bash
set -euo pipefail

# Mock rationale: This test uses 'terraform plan' which is an offline operation.
# It simulates infrastructure changes without interacting with actual cloud resources.
# 'jq' is used to parse the JSON output of the plan, allowing deterministic assertions
# on the planned resource properties without requiring AWS credentials or live infrastructure.

echo "--- Running Terraform module tests ---"

# Create a temporary directory for Terraform execution
TEST_DIR=$(mktemp -d)
cp -R ../src/* "$TEST_DIR/"
cp tests/fixtures/test.tfvars "$TEST_DIR/"

cd "$TEST_DIR"

# Initialize Terraform
echo "Initializing Terraform..."
terraform init -backend=false > /dev/null # -backend=false for offline testing
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

# Generate a plan and output it as JSON
echo "Generating Terraform plan..."
terraform plan -var-file=test.tfvars -out=tfplan > /dev/null
if [ $? -ne 0 ]; then
    echo "Terraform plan failed!"
    exit 1
fi
echo "Terraform plan generated."

# Show the plan in JSON format
PLAN_JSON=$(terraform show -json tfplan)

# --- Assertions ---

echo "Performing assertions on the plan..."

# 1. Check if the S3 bucket resource exists
BUCKET_RESOURCE=$(echo "$PLAN_JSON" | jq -r '.resource_changes[] | select(.type == "aws_s3_bucket" and .name == "whispering_log_archive")')
if [ -z "$BUCKET_RESOURCE" ]; then
    echo "Test Failed: S3 bucket 'aws_s3_bucket.whispering_log_archive' not found in plan."
    exit 1
fi
echo "Assertion Passed: S3 bucket resource found."

# 2. Check if the bucket name is correct from tfvars
PLANNED_BUCKET_NAME=$(echo "$BUCKET_RESOURCE" | jq -r '.change.after.bucket')
EXPECTED_BUCKET_NAME="test-whispering-log-archive"
if [ "$PLANNED_BUCKET_NAME" != "$EXPECTED_BUCKET_NAME" ]; then
    echo "Test Failed: Expected bucket name '$EXPECTED_BUCKET_NAME', got '$PLANNED_BUCKET_NAME'."
    exit 1
fi
echo "Assertion Passed: Bucket name is correct."

# 3. Check if public access is blocked
PUBLIC_ACCESS_BLOCK_RESOURCE=$(echo "$PLAN_JSON" | jq -r '.resource_changes[] | select(.type == "aws_s3_bucket_public_access_block" and .name == "whispering_log_archive")')
if [ -z "$PUBLIC_ACCESS_BLOCK_RESOURCE" ]; then
    echo "Test Failed: S3 public access block resource not found."
    exit 1
fi

BLOCK_PUBLIC_ACLS=$(echo "$PUBLIC_ACCESS_BLOCK_RESOURCE" | jq -r '.change.after.block_public_acls')
BLOCK_PUBLIC_AND_CROSS_ACCOUNT_ACCESS=$(echo "$PUBLIC_ACCESS_BLOCK_RESOURCE" | jq -r '.change.after.block_public_and_cross_account_access')
IGNORE_PUBLIC_ACLS=$(echo "$PUBLIC_ACCESS_BLOCK_RESOURCE" | jq -r '.change.after.ignore_public_acls')
RESTRICT_PUBLIC_BUCKETS=$(echo "$PUBLIC_ACCESS_BLOCK_RESOURCE" | jq -r '.change.after.restrict_public_buckets')

if [ "$BLOCK_PUBLIC_ACLS" != "true" ] || \
   [ "$BLOCK_PUBLIC_AND_CROSS_ACCOUNT_ACCESS" != "true" ] || \
   [ "$IGNORE_PUBLIC_ACLS" != "true" ] || \
   [ "$RESTRICT_PUBLIC_BUCKETS" != "true" ]; then
    echo "Test Failed: Public access block settings are incorrect."
    echo "  block_public_acls: $BLOCK_PUBLIC_ACLS (expected true)"
    echo "  block_public_and_cross_account_access: $BLOCK_PUBLIC_AND_CROSS_ACCOUNT_ACCESS (expected true)"
    echo "  ignore_public_acls: $IGNORE_PUBLIC_ACLS (expected true)"
    echo "  restrict_public_buckets: $RESTRICT_PUBLIC_BUCKETS (expected true)"
    exit 1
fi
echo "Assertion Passed: Public access is correctly blocked."

# 4. Check if lifecycle rule for expiration exists and is correct
LIFECYCLE_RESOURCE=$(echo "$PLAN_JSON" | jq -r '.resource_changes[] | select(.type == "aws_s3_bucket_lifecycle_configuration" and .name == "whispering_log_archive")')
if [ -z "$LIFECYCLE_RESOURCE" ]; then
    echo "Test Failed: S3 lifecycle configuration resource not found."
    exit 1
fi

EXPIRATION_DAYS=$(echo "$LIFECYCLE_RESOURCE" | jq -r '.change.after.rule[0].expiration[0].days')
EXPECTED_RETENTION_DAYS="3" # From test.tfvars
if [ "$EXPIRATION_DAYS" != "$EXPECTED_RETENTION_DAYS" ]; then
    echo "Test Failed: Expected expiration days '$EXPECTED_RETENTION_DAYS', got '$EXPIRATION_DAYS'."
    exit 1
fi
echo "Assertion Passed: Lifecycle rule for expiration after $EXPIRATION_DAYS days is correct."

echo "All tests passed successfully!"
cd - > /dev/null
rm -rf "$TEST_DIR"
