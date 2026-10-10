#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests..."

# Navigate to the test directory
cd "$(dirname "$0")"

# Initialize Terraform (downloads providers, etc.)
# Mock rationale: terraform init needs to run to set up the backend and download provider plugins.
# This is a prerequisite for `terraform plan` and does not interact with cloud APIs.
echo "Initializing Terraform..."
terraform init -backend=false > /dev/null

# Run terraform plan and capture output
# Mock rationale: terraform plan is run with -no-color and -detailed-exitcode to get a machine-readable
# output and exit code. This command performs a dry run without provisioning any actual resources,
# making it deterministic and offline. It only checks the syntax and the proposed changes.
echo "Running terraform plan..."
PLAN_OUTPUT=$(terraform plan -no-color -detailed-exitcode -out=tfplan 2>&1)
PLAN_EXIT_CODE=$?

# Check if plan was successful (exit code 0 means no changes, 2 means changes)
if [ "$PLAN_EXIT_CODE" -ne 0 ] && [ "$PLAN_EXIT_CODE" -ne 2 ]; then
  echo "Terraform plan failed with exit code $PLAN_EXIT_CODE"
  echo "$PLAN_OUTPUT"
  exit 1
fi

# Check for expected resources and properties in the plan output
echo "Verifying plan output..."

# Expect 4 resources to be added (bucket, versioning, SSE, public access block)
if ! echo "$PLAN_OUTPUT" | grep -q "Plan: 4 to add, 0 to change, 0 to destroy."; then
  echo "FAIL: Expected 'Plan: 4 to add, 0 to change, 0 to destroy.' not found."
  echo "$PLAN_OUTPUT"
  exit 1
fi

# Check for specific resource types and names
if ! echo "$PLAN_OUTPUT" | grep -q 'aws_s3_bucket.chronos_cache'; then
  echo "FAIL: aws_s3_bucket.chronos_cache not found in plan."
  exit 1
fi
if ! echo "$PLAN_OUTPUT" | grep -q 'aws_s3_bucket_versioning.chronos_cache_versioning'; then
  echo "FAIL: aws_s3_bucket_versioning.chronos_cache_versioning not found in plan."
  exit 1
fi
if ! echo "$PLAN_OUTPUT" | grep -q 'aws_s3_bucket_server_side_encryption_configuration.chronos_cache_sse'; then
  echo "FAIL: aws_s3_bucket_server_side_encryption_configuration.chronos_cache_sse not found in plan."
  exit 1
fi
if ! echo "$PLAN_OUTPUT" | grep -q 'aws_s3_bucket_public_access_block.chronos_cache_public_access_block'; then
  echo "FAIL: aws_s3_bucket_public_access_block.chronos_cache_public_access_block not found in plan."
  exit 1
fi

# Check for specific attributes (e.g., versioning enabled, SSE AES256, public access blocked)
if ! echo "$PLAN_OUTPUT" | grep -q 'versioning_configuration.0.status = "Enabled"'; then
  echo "FAIL: Versioning not enabled in plan."
  exit 1
fi
if ! echo "$PLAN_OUTPUT" | grep -q 'apply_server_side_encryption_by_default.0.sse_algorithm = "AES256"'; then
  echo "FAIL: SSE AES256 not configured in plan."
  exit 1
fi
if ! echo "$PLAN_OUTPUT" | grep -q 'block_public_acls = true'; then
  echo "FAIL: block_public_acls not true in plan."
  exit 1
fi
if ! echo "$PLAN_OUTPUT" | grep -q 'block_public_policy = true'; then
  echo "FAIL: block_public_policy not true in plan."
  exit 1
fi

echo "All Terraform plan checks passed successfully!"
exit 0
