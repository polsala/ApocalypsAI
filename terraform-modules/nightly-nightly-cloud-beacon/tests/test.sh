#!/bin/bash

set -euo pipefail

# Mock rationale: This test is designed to be deterministic and offline.
# It uses 'terraform plan' to verify the structure of the infrastructure
# that *would* be created, without actually interacting with AWS APIs.
# The AWS provider in main.tf is configured with dummy credentials to allow
# 'terraform plan' to proceed without live authentication.

echo "Running Nightly Cloud Beacon Terraform module tests..."

# Ensure Terraform is installed
if ! command -v terraform &> /dev/null
then
    echo "Error: Terraform is not installed. Please install Terraform to run tests."
    exit 1
fi

# Navigate to the tests directory
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPT_DIR"

# Initialize Terraform
echo "Initializing Terraform..."
terraform init -backend=false # Disable backend to ensure offline test

# Run terraform plan and capture output
echo "Running terraform plan..."
PLAN_OUTPUT=$(terraform plan -no-color -input=false 2>&1)
PLAN_EXIT_CODE=$?

if [ $PLAN_EXIT_CODE -ne 0 ]; then
    echo "Error: terraform plan failed with exit code $PLAN_EXIT_CODE."
    echo "Plan output:"
    echo "$PLAN_OUTPUT"
    exit 1
fi

# Assertions

# Check for S3 bucket resource
if ! echo "$PLAN_OUTPUT" | grep -q "aws_s3_bucket.beacon_bucket"; then
    echo "Error: S3 bucket resource (aws_s3_bucket.beacon_bucket) not found in plan."
    echo "Plan output:"
    echo "$PLAN_OUTPUT"
    exit 1
fi

# Check for S3 bucket policy resource
if ! echo "$PLAN_OUTPUT" | grep -q "aws_s3_bucket_policy.beacon_bucket_policy"; then
    echo "Error: S3 bucket policy resource (aws_s3_bucket_policy.beacon_bucket_policy) not found in plan."
    echo "Plan output:"
    echo "$PLAN_OUTPUT"
    exit 1
fi

# Check for CloudFront Origin Access Control resource
if ! echo "$PLAN_OUTPUT" | grep -q "aws_cloudfront_origin_access_control.beacon_oac"; then
    echo "Error: CloudFront Origin Access Control (aws_cloudfront_origin_access_control.beacon_oac) not found in plan."
    echo "Plan output:"
    echo "$PLAN_OUTPUT"
    exit 1
fi

# Check for CloudFront distribution resource
if ! echo "$PLAN_OUTPUT" | grep -q "aws_cloudfront_distribution.beacon_distribution"; then
    echo "Error: CloudFront distribution resource (aws_cloudfront_distribution.beacon_distribution) not found in plan."
    echo "Plan output:"
    echo "$PLAN_OUTPUT"
    exit 1
fi

# Check for S3 bucket object (index.html)
if ! echo "$PLAN_OUTPUT" | grep -q "aws_s3_bucket_object.beacon_index_html"; then
    echo "Error: S3 bucket object (aws_s3_bucket_object.beacon_index_html) not found in plan."
    echo "Plan output:"
    echo "$PLAN_OUTPUT"
    exit 1
fi

# Check for random_string resource (used for unique bucket naming)
if ! echo "$PLAN_OUTPUT" | grep -q "random_string.suffix"; then
    echo "Error: random_string.suffix resource not found in plan."
    echo "Plan output:"
    echo "$PLAN_OUTPUT"
    exit 1
fi

echo "All Nightly Cloud Beacon Terraform module tests passed successfully!"
