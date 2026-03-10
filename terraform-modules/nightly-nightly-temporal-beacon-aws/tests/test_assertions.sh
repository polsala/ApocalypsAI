#!/bin/bash
set -euo pipefail

# Mock rationale: This script performs offline, deterministic testing by
# inspecting the output of 'terraform plan'. It does not provision any
# cloud resources, thus requiring no actual AWS credentials or network access.

echo "--- Running Terraform module tests ---"

TEST_DIR=$(mktemp -d)
trap "rm -rf $TEST_DIR" EXIT

cp test_plan.tf "$TEST_DIR/"
cp -r ../src "$TEST_DIR/src"

cd "$TEST_DIR"

echo "Initializing Terraform..."
terraform init -backend=false > /dev/null # -backend=false for offline testing
if [ $? -ne 0 ]; then
    echo "ERROR: Terraform init failed."
    exit 1
fi

echo "Generating Terraform plan..."
terraform plan -out=tfplan.binary > /dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Terraform plan failed."
    exit 1
fi

echo "Inspecting plan for assertions..."
PLAN_JSON=$(terraform show -json tfplan.binary)

# Assert S3 bucket resource creation
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.actions[] == "create")' > /dev/null; then
    echo "FAIL: aws_s3_bucket resource not found in plan or not marked for creation."
    exit 1
fi
echo "PASS: aws_s3_bucket resource found and marked for creation."

# Assert S3 bucket versioning enabled
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_versioning" and .change.actions[] == "create" and .change.after.versioning_configuration.status == "Enabled")' > /dev/null; then
    echo "FAIL: aws_s3_bucket_versioning resource not found or not enabled."
    exit 1
fi
echo "PASS: aws_s3_bucket_versioning enabled."

# Assert S3 bucket server-side encryption enabled (AES256)
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_server_side_encryption_configuration" and .change.actions[] == "create" and .change.after.rule[0].apply_server_side_encryption_by_default.sse_algorithm == "AES256")' > /dev/null; then
    echo "FAIL: aws_s3_bucket_server_side_encryption_configuration not found or not AES256."
    exit 1
fi
echo "PASS: aws_s3_bucket_server_side_encryption_configuration set to AES256."

# Assert S3 bucket public access block is configured
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_public_access_block" and .change.actions[] == "create" and .change.after.block_public_acls == true and .change.after.block_public_policy == true and .change.after.ignore_public_acls == true and .change.after.restrict_public_buckets == true)' > /dev/null; then
    echo "FAIL: aws_s3_bucket_public_access_block not found or not fully configured."
    exit 1
fi
echo "PASS: aws_s3_bucket_public_access_block fully configured."

# Assert tags are present on the bucket
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.after.tags.Purpose == "TemporalAnomalyBeacon" and .change.after.tags.Environment == "test" and .change.after.tags.ManagedBy == "ApocalypsAI")' > /dev/null; then
    echo "FAIL: Expected tags (Purpose, Environment, ManagedBy) not found on S3 bucket."
    exit 1
fi
echo "PASS: Expected tags found on S3 bucket."

echo "All Terraform module tests passed successfully!"
