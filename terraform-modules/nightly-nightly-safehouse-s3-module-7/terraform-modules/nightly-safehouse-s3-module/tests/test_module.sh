#!/usr/bin/env bash
set -e

# Mock rationale: This test runs terraform init/validate on the module without contacting AWS.
# It uses -backend=false to avoid remote state and ensures the configuration is syntactically correct.

cd "$(dirname "$0")/../src"

# Initialise Terraform (no backend) and validate syntax
terraform init -backend=false > /dev/null 2>&1
terraform validate > /dev/null

# Verify that required resources are present in the configuration
grep -q 'resource "aws_s3_bucket" "safehouse"' main.tf
grep -q 'resource "aws_s3_bucket_versioning" "safehouse"' main.tf
grep -q 'resource "aws_s3_bucket_server_side_encryption_configuration" "safehouse"' main.tf
grep -q 'resource "aws_s3_bucket_lifecycle_configuration" "safehouse"' main.tf
grep -q 'resource "random_id" "cache"' main.tf

echo "All checks passed."
