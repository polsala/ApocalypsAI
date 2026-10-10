#!/usr/bin/env bash
set -e

# Mock rationale: Ensure required resources are defined in main.tf
required=("aws_s3_bucket.this" "aws_s3_bucket_versioning.this" "aws_s3_bucket_server_side_encryption_configuration.this" "aws_s3_bucket_public_access_block.this")

for r in "${required[@]}"; do
  if ! grep -q "$r" "$(dirname "$0")/../main.tf"; then
    echo "Missing resource $r"
    exit 1
  fi
done

echo "All required resources present."
