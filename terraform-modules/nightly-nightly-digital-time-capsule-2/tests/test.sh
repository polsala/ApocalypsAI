#!/bin/bash
set -euo pipefail

# Ensure Terraform is installed
if ! command -v terraform &> /dev/null
then
    echo "Terraform could not be found. Please install it to run tests."
    exit 1
fi

echo "Running Terraform validation..."
# Mock rationale: Initialize without a backend to perform local validation without requiring AWS credentials or state storage.
terraform -chdir=tests init -backend=false
terraform -chdir=tests validate

echo "Running Terraform plan (no actual apply)..."
# Mock rationale: Use -no-color and grep to check for expected resource creation in the plan output.
# This is an offline, deterministic check of the plan's structure without interacting with AWS APIs.
PLAN_OUTPUT=$(terraform -chdir=tests plan -out=tfplan -no-color)

# Check for the creation of the S3 bucket
if echo "$PLAN_OUTPUT" | grep -q "aws_s3_bucket.time_capsule will be created"; then
    echo "PASS: S3 bucket creation detected in plan."
else
    echo "FAIL: S3 bucket creation NOT detected in plan."
    exit 1
fi

# Check for the creation of S3 bucket versioning
if echo "$PLAN_OUTPUT" | grep -q "aws_s3_bucket_versioning.time_capsule_versioning will be created"; then
    echo "PASS: S3 bucket versioning detected in plan."
else
    echo "FAIL: S3 bucket versioning NOT detected in plan."
    exit 1
fi

# Check for the creation of S3 bucket lifecycle configuration (only if enabled)
if echo "$PLAN_OUTPUT" | grep -q "aws_s3_bucket_lifecycle_configuration.time_capsule_lifecycle[0] will be created"; then
    echo "PASS: S3 bucket lifecycle configuration detected in plan (when enabled)."
else
    echo "FAIL: S3 bucket lifecycle configuration NOT detected in plan (when enabled)."
    exit 1
fi

# Check for public access block
if echo "$PLAN_OUTPUT" | grep -q "aws_s3_bucket_public_access_block.time_capsule_public_access_block will be created"; then
    echo "PASS: S3 public access block detected in plan."
else
    echo "FAIL: S3 public access block NOT detected in plan."
    exit 1
fi

# Check for server-side encryption
if echo "$PLAN_OUTPUT" | grep -q "aws_s3_bucket_server_side_encryption_configuration.time_capsule_encryption will be created"; then
    echo "PASS: S3 server-side encryption detected in plan."
else
    echo "FAIL: S3 server-side encryption NOT detected in plan."
    exit 1
fi

echo "All Terraform tests passed!"
rm tfplan # Clean up the generated plan file
