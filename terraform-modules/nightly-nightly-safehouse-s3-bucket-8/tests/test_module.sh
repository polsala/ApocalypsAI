#!/usr/bin/env bash
# Test script for nightly-safehouse-s3-bucket Terraform module
# Mock rationale: we cannot run real AWS, so we validate Terraform syntax and presence of resources.

set -e

# Initialize a temporary directory
TMPDIR=$(mktemp -d)
cp -R . "$TMPDIR/module"
cd "$TMPDIR/module"

# Initialize Terraform (no backend)
terraform init -input=false -backend=false > /dev/null

# Validate configuration
terraform validate > /dev/null

# Check that required resources are defined
grep -q 'resource "aws_s3_bucket"' main.tf || { echo "Missing aws_s3_bucket"; exit 1; }
grep -q 'resource "aws_s3_bucket_versioning"' main.tf || { echo "Missing versioning"; exit 1; }
grep -q 'resource "aws_s3_bucket_server_side_encryption_configuration"' main.tf || { echo "Missing encryption"; exit 1; }
grep -q 'resource "aws_s3_bucket_lifecycle_configuration"' main.tf || { echo "Missing lifecycle"; exit 1; }

echo "All checks passed."
