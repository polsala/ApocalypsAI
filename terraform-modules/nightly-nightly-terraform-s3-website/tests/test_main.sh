#!/usr/bin/env bash
set -e

# Mock rationale: Verify that the Terraform module defines required resources.

FILE="src/main.tf"

# Check for S3 bucket resource
if ! grep -q 'resource "aws_s3_bucket" "website"' "$FILE"; then
  echo "FAIL: aws_s3_bucket resource not found"
  exit 1
fi

# Check for website configuration block
if ! grep -q 'website {' "$FILE"; then
  echo "FAIL: website configuration block not found"
  exit 1
fi

# Check for CloudFront distribution resource (optional but should exist in the module)
if ! grep -q 'resource "aws_cloudfront_distribution" "cdn"' "$FILE"; then
  echo "FAIL: aws_cloudfront_distribution resource not found"
  exit 1
fi

echo "PASS: All required resources are present"
