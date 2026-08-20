#!/bin/bash
set -euo pipefail

echo "Running Terraform plan for validation..."

# Initialize Terraform in the test directory
terraform -chdir=tests init -backend=false -input=false > /dev/null
# Mock rationale: -backend=false ensures no state backend is configured,
# and -input=false prevents interactive prompts, making it deterministic.

# Generate a plan and output it as JSON
PLAN_OUTPUT=$(terraform -chdir=tests plan -out=tfplan -json -input=false)
# Mock rationale: -json output allows programmatic inspection of the plan
# without requiring actual resource creation. This makes the test offline and deterministic.

# Check if the plan command was successful
if [ $? -ne 0 ]; then
  echo "Terraform plan failed!"
  echo "$PLAN_OUTPUT"
  exit 1
fi

echo "Parsing plan output..."

# Verify bucket creation
BUCKET_CREATED=$(echo "$PLAN_OUTPUT" | jq -r '.resource_changes[]? | select(.address == "aws_s3_bucket.cache_vault") | .change.actions[]')
if [[ "$BUCKET_CREATED" != "create" ]]; then
  echo "Test failed: S3 bucket 'aws_s3_bucket.cache_vault' not planned for creation."
  exit 1
fi

# Verify versioning is enabled
VERSIONING_ENABLED=$(echo "$PLAN_OUTPUT" | jq -r '.resource_changes[]? | select(.address == "aws_s3_bucket_versioning.cache_vault_versioning") | .change.after.versioning_configuration[0].status')
if [[ "$VERSIONING_ENABLED" != "Enabled" ]]; then
  echo "Test failed: S3 bucket versioning not enabled. Got: $VERSIONING_ENABLED"
  exit 1
fi

# Verify server-side encryption is AES256
SSE_ALGORITHM=$(echo "$PLAN_OUTPUT" | jq -r '.resource_changes[]? | select(.address == "aws_s3_bucket_server_side_encryption_configuration.cache_vault_encryption") | .change.after.rule[0].apply_server_side_encryption_by_default[0].sse_algorithm')
if [[ "$SSE_ALGORITHM" != "AES256" ]]; then
  echo "Test failed: S3 bucket server-side encryption not set to AES256. Got: $SSE_ALGORITHM"
  exit 1
fi

# Verify lifecycle rules for transitions and expiration
LIFECYCLE_RULE=$(echo "$PLAN_OUTPUT" | jq -r '.resource_changes[]? | select(.address == "aws_s3_bucket_lifecycle_configuration.cache_vault_lifecycle") | .change.after.rule[0]')

TRANSITION_STANDARD_IA_DAYS=$(echo "$LIFECYCLE_RULE" | jq -r '.transition[]? | select(.storage_class == "STANDARD_IA") | .days')
if [[ "$TRANSITION_STANDARD_IA_DAYS" != "15" ]]; then
  echo "Test failed: Lifecycle rule for STANDARD_IA transition days is incorrect. Expected 15, got $TRANSITION_STANDARD_IA_DAYS"
  exit 1
fi

TRANSITION_GLACIER_DAYS=$(echo "$LIFECYCLE_RULE" | jq -r '.transition[]? | select(.storage_class == "GLACIER") | .days')
if [[ "$TRANSITION_GLACIER_DAYS" != "60" ]]; then
  echo "Test failed: Lifecycle rule for GLACIER transition days is incorrect. Expected 60, got $TRANSITION_GLACIER_DAYS"
  exit 1
fi

EXPIRATION_DAYS=$(echo "$LIFECYCLE_RULE" | jq -r '.expiration[0].days')
if [[ "$EXPIRATION_DAYS" != "180" ]]; then
  echo "Test failed: Lifecycle rule for expiration days is incorrect. Expected 180, got $EXPIRATION_DAYS"
  exit 1
fi

NONCURRENT_VERSION_EXPIRATION_DAYS=$(echo "$LIFECYCLE_RULE" | jq -r '.noncurrent_version_expiration[0].days')
if [[ "$NONCURRENT_VERSION_EXPIRATION_DAYS" != "180" ]]; then
  echo "Test failed: Lifecycle rule for noncurrent version expiration days is incorrect. Expected 180, got $NONCURRENT_VERSION_EXPIRATION_DAYS"
  exit 1
fi

echo "All Terraform plan validations passed!"
exit 0
