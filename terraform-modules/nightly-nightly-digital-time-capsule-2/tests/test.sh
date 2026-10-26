#!/bin/bash
set -euo pipefail

echo "Initializing Terraform..."
terraform -chdir=tests init -backend=false -input=false > /dev/null

echo "Generating Terraform plan..."
terraform -chdir=tests plan -out=tfplan -input=false > /dev/null

echo "Inspecting Terraform plan..."
PLAN_JSON=$(terraform -chdir=tests show -json tfplan)

# Mock rationale: This test is deterministic and offline because it only
# inspects the JSON output of 'terraform plan'. It does not interact with
# any cloud provider APIs. 'terraform init -backend=false' ensures no state
# backend is configured, and '-input=false' prevents interactive prompts.
# The 'provider "aws"' block in tests/main.tf is purely for syntax validation
# by Terraform and does not require actual AWS credentials for 'plan' and 'show'.

# Check if the S3 bucket resource is present
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.actions[] == "create")' > /dev/null; then
  echo "Test Failed: aws_s3_bucket resource not found in plan."
  exit 1
fi
echo "  - Verified: aws_s3_bucket resource exists."

# Check bucket name
BUCKET_NAME=$(echo "$PLAN_JSON" | jq -r '.resource_changes[] | select(.type == "aws_s3_bucket").change.after.bucket')
if [ "$BUCKET_NAME" != "test-apocalypsai-time-capsule-12345" ]; then
  echo "Test Failed: Incorrect bucket name. Expected 'test-apocalypsai-time-capsule-12345', got '$BUCKET_NAME'."
  exit 1
fi
echo "  - Verified: Bucket name is correct."

# Check versioning enabled
VERSIONING_ENABLED=$(echo "$PLAN_JSON" | jq -r '.resource_changes[] | select(.type == "aws_s3_bucket").change.after.versioning[0].enabled')
if [ "$VERSIONING_ENABLED" != "true" ]; then
  echo "Test Failed: Versioning not enabled."
  exit 1
fi
echo "  - Verified: Versioning is enabled."

# Check object lock configuration
OBJECT_LOCK_ENABLED=$(echo "$PLAN_JSON" | jq -r '.resource_changes[] | select(.type == "aws_s3_bucket").change.after.object_lock_configuration[0].object_lock_enabled')
OBJECT_LOCK_MODE=$(echo "$PLAN_JSON" | jq -r '.resource_changes[] | select(.type == "aws_s3_bucket").change.after.object_lock_configuration[0].rule[0].default_retention[0].mode')
OBJECT_LOCK_DAYS=$(echo "$PLAN_JSON" | jq -r '.resource_changes[] | select(.type == "aws_s3_bucket").change.after.object_lock_configuration[0].rule[0].default_retention[0].days')

if [ "$OBJECT_LOCK_ENABLED" != "Enabled" ] || [ "$OBJECT_LOCK_MODE" != "COMPLIANCE" ] || [ "$OBJECT_LOCK_DAYS" != "365" ]; then
  echo "Test Failed: Object lock configuration incorrect."
  echo "  Expected: Enabled=Enabled, Mode=COMPLIANCE, Days=365"
  echo "  Got: Enabled=$OBJECT_LOCK_ENABLED, Mode=$OBJECT_LOCK_MODE, Days=$OBJECT_LOCK_DAYS"
  exit 1
fi
echo "  - Verified: Object lock is configured correctly (COMPLIANCE, 365 days)."

# Check lifecycle rule for deep archive transition
LIFECYCLE_TRANSITION_DAYS=$(echo "$PLAN_JSON" | jq -r '.resource_changes[] | select(.type == "aws_s3_bucket").change.after.lifecycle_rule[] | select(.id == "deep_archive_transition").transition[0].days')
LIFECYCLE_STORAGE_CLASS=$(echo "$PLAN_JSON" | jq -r '.resource_changes[] | select(.type == "aws_s3_bucket").change.after.lifecycle_rule[] | select(.id == "deep_archive_transition").transition[0].storage_class')

if [ "$LIFECYCLE_TRANSITION_DAYS" != "30" ] || [ "$LIFECYCLE_STORAGE_CLASS" != "GLACIER_DEEP_ARCHIVE" ]; then
  echo "Test Failed: Lifecycle rule for deep archive transition incorrect."
  echo "  Expected: Days=30, StorageClass=GLACIER_DEEP_ARCHIVE"
  echo "  Got: Days=$LIFECYCLE_TRANSITION_DAYS, StorageClass=$LIFECYCLE_STORAGE_CLASS"
  exit 1
fi
echo "  - Verified: Lifecycle rule for GLACIER_DEEP_ARCHIVE transition is correct (30 days)."

# Check public access block
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_public_access_block" and .change.actions[] == "create" and .change.after.block_public_acls == true and .change.after.block_public_policy == true and .change.after.ignore_public_acls == true and .change.after.restrict_public_buckets == true)' > /dev/null; then
  echo "Test Failed: aws_s3_bucket_public_access_block resource not found or incorrectly configured."
  exit 1
fi
echo "  - Verified: Public access block is configured."

# Check server-side encryption
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_server_side_encryption_configuration" and .change.actions[] == "create" and .change.after.rule[0].apply_server_side_encryption_by_default[0].sse_algorithm == "AES256")' > /dev/null; then
  echo "Test Failed: aws_s3_bucket_server_side_encryption_configuration resource not found or incorrectly configured."
  exit 1
fi
echo "  - Verified: Server-side encryption (AES256) is configured."

echo "All tests passed!"
