#!/usr/bin/env bash
set -e
# Mock rationale: Ensure the Terraform module defines an aws_s3_bucket resource.
if grep -q 'resource "aws_s3_bucket"' main.tf; then
  echo "PASS"
else
  echo "FAIL"
  exit 1
fi
