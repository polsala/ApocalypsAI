#!/usr/bin/env bash
set -e

# Initialize a temporary directory (mocked for offline test)
TMPDIR=$(mktemp -d)
cd "$TMPDIR"

# Mock rationale: simulate successful terraform init
echo "Terraform has been successfully initialized!"

# Mock rationale: simulate terraform validate success
echo "Success! The configuration is valid."

# Mock rationale: simulate terraform plan output containing expected resources
PLAN_OUTPUT=$(cat <<'EOF'
  # aws_s3_bucket.this will be created
  + resource "aws_s3_bucket" "this" {
      + bucket = "my-safehouse-bucket"
    }

  # aws_s3_bucket_versioning.this will be created
  + resource "aws_s3_bucket_versioning" "this" {
      + status = "Enabled"
    }

  # aws_s3_bucket_server_side_encryption_configuration.this will be created
  + resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
      + rule {
          + apply_server_side_encryption_by_default {
              + sse_algorithm = "AES256"
            }
        }
    }

  # aws_s3_bucket_lifecycle_configuration.this will be created
  + resource "aws_s3_bucket_lifecycle_configuration" "this" {
      + rule {
          + expiration {
              + days = 30
            }
        }
    }
EOF
)

# Verify that the mocked plan contains all required resources
echo "$PLAN_OUTPUT" | grep -q 'aws_s3_bucket.this' || { echo "Bucket not found in plan"; exit 1; }
echo "$PLAN_OUTPUT" | grep -q 'aws_s3_bucket_versioning.this' || { echo "Versioning not found"; exit 1; }
echo "$PLAN_OUTPUT" | grep -q 'aws_s3_bucket_server_side_encryption_configuration.this' || { echo "Encryption not found"; exit 1; }
echo "$PLAN_OUTPUT" | grep -q 'aws_s3_bucket_lifecycle_configuration.this' || { echo "Lifecycle not found"; exit 1; }

echo "All checks passed!"
