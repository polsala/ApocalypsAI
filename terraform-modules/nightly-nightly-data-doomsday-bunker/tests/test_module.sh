#!/bin/bash
set -euo pipefail

# Mock rationale: This test script performs static analysis and HCL validation
# without provisioning any cloud resources. It simulates a successful Terraform
# module setup and verifies the presence of key configuration elements offline.

echo "Running Terraform module tests..."

# Create a temporary directory for testing
TEST_DIR=$(mktemp -d)
trap "rm -rf $TEST_DIR" EXIT # Clean up on exit

echo "Temporary test directory: $TEST_DIR"

# Copy module files to the temporary directory
cp ../*.tf "$TEST_DIR/"

cd "$TEST_DIR"

echo "Initializing Terraform (offline)..."
# terraform init -backend=false is crucial for offline testing
if ! terraform init -backend=false; then
    echo "ERROR: Terraform initialization failed."
    exit 1
fi
echo "Terraform initialized successfully."

echo "Validating Terraform HCL syntax..."
if ! terraform validate; then
    echo "ERROR: Terraform HCL validation failed."
    exit 1
fi
echo "Terraform HCL validated successfully."

echo "Checking Terraform HCL formatting..."
if ! terraform fmt -check=true; then
    echo "ERROR: Terraform HCL formatting check failed. Run 'terraform fmt'."
    exit 1
fi
echo "Terraform HCL formatting is correct."

echo "Verifying essential S3 bucket configurations..."

# Check for S3 bucket resource
if ! grep -q 'resource "aws_s3_bucket" "doomsday_bunker"' main.tf; then
    echo "ERROR: S3 bucket resource 'aws_s3_bucket.doomsday_bunker' not found."
    exit 1
fi
echo "S3 bucket resource found."

# Check for versioning
if ! grep -q 'resource "aws_s3_bucket_versioning" "doomsday_bunker_versioning"' main.tf; then
    echo "ERROR: S3 bucket versioning resource not found."
    exit 1
fi
echo "S3 bucket versioning resource found."

# Check for server-side encryption
if ! grep -q 'resource "aws_s3_bucket_server_side_encryption_configuration" "doomsday_bunker_encryption"' main.tf; then
    echo "ERROR: S3 bucket encryption resource not found."
    exit 1
fi
echo "S3 bucket encryption resource found."

# Check for public access block
if ! grep -q 'resource "aws_s3_bucket_public_access_block" "doomsday_bunker_public_access_block"' main.tf; then
    echo "ERROR: S3 bucket public access block resource not found."
    exit 1
fi
echo "S3 bucket public access block resource found."

echo "All essential configurations verified."
echo "Terraform module tests passed successfully!"
