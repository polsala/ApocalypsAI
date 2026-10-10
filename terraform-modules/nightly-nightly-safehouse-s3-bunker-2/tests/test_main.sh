#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Ensure the Terraform module defines expected resources without contacting AWS.

FILE="src/main.tf"

# Verify required providers are declared
grep -q 'source  = "hashicorp/aws"' "$FILE"
grep -q 'source  = "hashicorp/random"' "$FILE"

# Verify variable definition
grep -q 'variable "bucket_prefix"' "$FILE"

# Verify random_pet resource
grep -q 'resource "random_pet" "name"' "$FILE"

# Verify S3 bucket resource
grep -q 'resource "aws_s3_bucket" "bunker"' "$FILE"

# Verify versioning configuration
grep -q 'resource "aws_s3_bucket_versioning" "bunker_versioning"' "$FILE"

# Verify server‑side encryption configuration
grep -q 'resource "aws_s3_bucket_server_side_encryption_configuration" "bunker_encryption"' "$FILE"

# Verify lifecycle configuration
grep -q 'resource "aws_s3_bucket_lifecycle_configuration" "bunker_lifecycle"' "$FILE"

# Verify output definition
grep -q 'output "bucket_name"' "$FILE"

echo "All checks passed."
