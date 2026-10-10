#!/bin/bash
set -euo pipefail

echo "Running Terraform plan tests...\n"

# Create a temporary directory for Terraform execution
TEST_ROOT_DIR=$(mktemp -d)

# Setup the test environment: copy test config and module source
mkdir -p "$TEST_ROOT_DIR/modules/nightly-temporal-archive-vault"
cp tests/test_module.tf "$TEST_ROOT_DIR/main.tf"
cp src/*.tf "$TEST_ROOT_DIR/modules/nightly-temporal-archive-vault/"

cd "$TEST_ROOT_DIR"

# Initialize Terraform (backend=false for offline testing)
# Mock rationale: `terraform init -backend=false` performs local setup without contacting cloud providers.
# It downloads providers and validates module syntax, which is sufficient for offline testing of the module's structure.
terraform init -backend=false -input=false > /dev/null
if [ $? -ne 0 ]; then
  echo "Terraform init failed!"
  exit 1
fi

# Generate a plan in JSON format
# Mock rationale: `terraform plan -json` generates a detailed plan of changes without applying them.
# This output can be parsed to verify resource configurations, variable interpolations, and lifecycle rules
# without requiring actual AWS credentials or network access, making the test deterministic and offline.
PLAN_OUTPUT=$(terraform plan -out=tfplan.binary -json -input=false)
if [ $? -ne 0 ]; then
  echo "Terraform plan failed!"
  echo "$PLAN_OUTPUT"
  exit 1
fi

# Test 1: Check if the main bucket is planned with the correct name
BUCKET_NAME_1=$(echo "$PLAN_OUTPUT" | jq -r '.resource_changes[] | select(.address == "module.temporal_archive_test.aws_s3_bucket.archive_vault") | .change.after.bucket')
if [ "$BUCKET_NAME_1" != "apocalypsai-test-archive-vault-12345" ]; then
  echo "Test Failed: Bucket name for temporal_archive_test mismatch. Expected 'apocalypsai-test-archive-vault-12345', got '$BUCKET_NAME_1'"
  exit 1
fi
echo "Test Passed: Bucket name for temporal_archive_test is correct."

# Test 2: Check if versioning is enabled
VERSIONING_STATUS=$(echo "$PLAN_OUTPUT" | jq -r '.resource_changes[] | select(.address == "module.temporal_archive_test.aws_s3_bucket_versioning.archive_vault_versioning") | .change.after.versioning_configuration[0].status')
if [ "$VERSIONING_STATUS" != "Enabled" ]; then
  echo "Test Failed: Versioning status mismatch. Expected 'Enabled', got '$VERSIONING_STATUS'"
  exit 1
fi
echo "Test Passed: Versioning is enabled."

# Test 3: Check if public access is blocked
BLOCK_PUBLIC_ACLS=$(echo "$PLAN_OUTPUT" | jq -r '.resource_changes[] | select(.address == "module.temporal_archive_test.aws_s3_bucket_public_access_block.archive_vault_public_access_block") | .change.after.block_public_acls')
if [ "$BLOCK_PUBLIC_ACLS" != "true" ]; then
  echo "Test Failed: Block public ACLs mismatch. Expected 'true', got '$BLOCK_PUBLIC_ACLS'"
  exit 1
fi
echo "Test Passed: Public ACLs are blocked."

# Test 4: Check lifecycle rule for GLACIER_IR transition days
GLACIER_IR_DAYS=$(echo "$PLAN_OUTPUT" | jq -r '.resource_changes[] | select(.address == "module.temporal_archive_test.aws_s3_bucket_lifecycle_configuration.archive_vault_lifecycle") | .change.after.rule[0].transition[] | select(.storage_class == "GLACIER_IR") | .days')
if [ "$GLACIER_IR_DAYS" != "60" ]; then
  echo "Test Failed: GLACIER_IR transition days mismatch. Expected '60', got '$GLACIER_IR_DAYS'"
  exit 1
fi
echo "Test Passed: GLACIER_IR transition days are correct."

# Test 5: Check lifecycle rule for DEEP_ARCHIVE transition days
DEEP_ARCHIVE_DAYS=$(echo "$PLAN_OUTPUT" | jq -r '.resource_changes[] | select(.address == "module.temporal_archive_test.aws_s3_bucket_lifecycle_configuration.archive_vault_lifecycle") | .change.after.rule[0].transition[] | select(.storage_class == "DEEP_ARCHIVE") | .days')
if [ "$DEEP_ARCHIVE_DAYS" != "180" ]; then
  echo "Test Failed: DEEP_ARCHIVE transition days mismatch. Expected '180', got '$DEEP_ARCHIVE_DAYS'"
  exit 1
fi
echo "Test Passed: DEEP_ARCHIVE transition days are correct."

# Test 6: Check lifecycle rule for expiration days
EXPIRATION_DAYS=$(echo "$PLAN_OUTPUT" | jq -r '.resource_changes[] | select(.address == "module.temporal_archive_test.aws_s3_bucket_lifecycle_configuration.archive_vault_lifecycle") | .change.after.rule[0].expiration[0].days')
if [ "$EXPIRATION_DAYS" != "365" ]; then
  echo "Test Failed: Expiration days mismatch. Expected '365', got '$EXPIRATION_DAYS'"
  exit 1
fi
echo "Test Passed: Expiration days are correct."

# Test 7: Check for no expiration rule when expiration_days is null
BUCKET_NAME_2=$(echo "$PLAN_OUTPUT" | jq -r '.resource_changes[] | select(.address == "module.temporal_archive_no_expiration_test.aws_s3_bucket.archive_vault") | .change.after.bucket')
if [ "$BUCKET_NAME_2" != "apocalypsai-test-archive-vault-no-expire-67890" ]; then
  echo "Test Failed: Bucket name for temporal_archive_no_expiration_test mismatch."
  exit 1
fi
NO_EXPIRATION_RULE=$(echo "$PLAN_OUTPUT" | jq -r '.resource_changes[] | select(.address == "module.temporal_archive_no_expiration_test.aws_s3_bucket_lifecycle_configuration.archive_vault_lifecycle") | .change.after.rule[0].expiration | length')
if [ "$NO_EXPIRATION_RULE" != "0" ]; then
  echo "Test Failed: Expiration rule found for no_expiration_test. Expected 0, got '$NO_EXPIRATION_RULE'"
  exit 1
fi
echo "Test Passed: No expiration rule for no_expiration_test."


echo "\nAll Terraform plan tests passed!"

# Clean up temporary directory
rm -rf "$TEST_ROOT_DIR"
