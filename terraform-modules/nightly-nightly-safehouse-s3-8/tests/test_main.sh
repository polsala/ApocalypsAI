#!/usr/bin/env bash
set -e

# Mock rationale: Use local backend and dummy provider config; no real AWS calls.
terraform -chdir=../src init -backend=false > /dev/null

# Validate configuration
terraform -chdir=../src validate

# Generate a plan and capture output
PLAN_OUTPUT=$(terraform -chdir=../src plan -no-color -input=false -var='bucket_name_prefix=testsafehouse' 2>&1)

# Check that the plan includes an aws_s3_bucket resource
if echo "$PLAN_OUTPUT" | grep -q 'aws_s3_bucket.safehouse'; then
  echo "PASS: S3 bucket resource found in plan."
  exit 0
else
  echo "FAIL: S3 bucket resource not found."
  exit 1
fi
