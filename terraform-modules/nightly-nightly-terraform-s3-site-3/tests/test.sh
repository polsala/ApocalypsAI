#!/usr/bin/env bash
set -e

# Mock rationale: Verify that the Terraform module defines the expected resources and variables without invoking Terraform.

FILE="../src/main.tf"

# Check for aws_s3_bucket resource
grep -q 'resource "aws_s3_bucket" "static_site"' "$FILE"

# Check for website block
grep -q 'website {' "$FILE"

# Check for bucket_policy resource
grep -q 'resource "aws_s3_bucket_policy" "public_read"' "$FILE"

# Check for required variables
grep -q 'variable "bucket_name"' "$FILE"
grep -q 'variable "index_document"' "$FILE"
grep -q 'variable "error_document"' "$FILE"

echo "All checks passed."
