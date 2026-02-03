#!/usr/bin/env bash
set -e

# Mock rationale: Verify that the module defines required resources and variables without invoking Terraform.

# Check for S3 bucket resource
grep -q 'resource "aws_s3_bucket" "this"' src/main.tf || { echo "Missing aws_s3_bucket resource"; exit 1; }

# Check for versioning
grep -q 'resource "aws_s3_bucket_versioning" "this"' src/main.tf || { echo "Missing versioning resource"; exit 1; }

# Check for encryption
grep -q 'resource "aws_s3_bucket_server_side_encryption_configuration" "this"' src/main.tf || { echo "Missing encryption resource"; exit 1; }

# Check for lifecycle rule
grep -q 'resource "aws_s3_bucket_lifecycle_configuration" "this"' src/main.tf || { echo "Missing lifecycle resource"; exit 1; }

# Check for variable definitions
grep -q 'variable "bucket_name"' src/variables.tf || { echo "Missing bucket_name variable"; exit 1; }

echo "All checks passed."
