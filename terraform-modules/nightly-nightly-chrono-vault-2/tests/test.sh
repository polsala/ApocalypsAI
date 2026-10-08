#!/bin/bash
set -euo pipefail

echo "--- Running Terraform tests for nightly-chrono-vault ---"

# Change to the tests directory
cd "$(dirname "$0")"

# Initialize Terraform
echo "Initializing Terraform..."
terraform init -backend=false > /dev/null

# Generate a plan in JSON format
echo "Generating Terraform plan..."
PLAN_OUTPUT=$(terraform plan -no-color -input=false -out=tfplan -json)
# Mock rationale: terraform plan is run offline without actual cloud credentials.
# The output is then parsed to verify the configuration.

# Check for errors in plan generation
if [ $? -ne 0 ]; then
  echo "Terraform plan failed!"
  echo "$PLAN_OUTPUT"
  exit 1
fi

# Show the plan in JSON format for detailed inspection
PLAN_JSON=$(terraform show -json tfplan)

# --- Assertions ---

echo "Performing assertions on the plan..."

# 1. Assert bucket versioning is enabled for 'test_chrono_vault'
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.address == "module.test_chrono_vault.aws_s3_bucket_versioning.chrono_vault_versioning") | .change.after.versioning_configuration[0].status == "Enabled"' > /dev/null; then
  echo "FAIL: Versioning not enabled for test_chrono_vault."
  exit 1
fi
echo "PASS: Versioning enabled for test_chrono_vault."

# 2. Assert public access block is configured for 'test_chrono_vault'
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.address == "module.test_chrono_vault.aws_s3_bucket_public_access_block.chrono_vault_public_access_block") | .change.after.block_public_acls == true and .change.after.block_public_policy == true' > /dev/null; then
  echo "FAIL: Public access block not fully configured for test_chrono_vault."
  exit 1
fi
echo "PASS: Public access block configured for test_chrono_vault."

# 3. Assert lifecycle rules for 'test_chrono_vault'
# Check STANDARD_IA transition
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.address == "module.test_chrono_vault.aws_s3_bucket_lifecycle_configuration.chrono_vault_lifecycle") | .change.after.rule[0].transition[] | select(.storage_class == "STANDARD_IA") | .days == 45' > /dev/null; then
  echo "FAIL: STANDARD_IA transition days incorrect for test_chrono_vault."
  exit 1
fi
echo "PASS: STANDARD_IA transition days correct for test_chrono_vault."

# Check GLACIER transition
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.address == "module.test_chrono_vault.aws_s3_bucket_lifecycle_configuration.chrono_vault_lifecycle") | .change.after.rule[0].transition[] | select(.storage_class == "GLACIER") | .days == 120' > /dev/null; then
  echo "FAIL: GLACIER transition days incorrect for test_chrono_vault."
  exit 1
fi
echo "PASS: GLACIER transition days correct for test_chrono_vault."

# Check noncurrent version expiration (90 days * 2 = 180 days)
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.address == "module.test_chrono_vault.aws_s3_bucket_lifecycle_configuration.chrono_vault_lifecycle") | .change.after.rule[0].noncurrent_version_expiration[0].days == 180' > /dev/null; then
  echo "FAIL: Noncurrent version expiration days incorrect for test_chrono_vault."
  exit 1
fi
echo "PASS: Noncurrent version expiration days correct for test_chrono_vault."

# 4. Assert server-side encryption (SSE-S3 by default) for 'test_chrono_vault'
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.address == "module.test_chrono_vault.aws_s3_bucket_server_side_encryption_configuration.chrono_vault_encryption") | .change.after.rule[0].apply_server_side_encryption_by_default[0].sse_algorithm == "AES256"' > /dev/null; then
  echo "FAIL: SSE-S3 encryption not configured for test_chrono_vault."
  exit 1
fi
echo "PASS: SSE-S3 encryption configured for test_chrono_vault."

# 5. Assert access logging resource is created for 'test_chrono_vault'
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.address == "module.test_chrono_vault.aws_s3_bucket_logging.chrono_vault_logging[0]") | .change.actions | contains(["create"])' > /dev/null; then
  echo "FAIL: Access logging resource not created for test_chrono_vault."
  exit 1
fi
echo "PASS: Access logging resource created for test_chrono_vault."

# 6. Assert access logging resource is NOT created for 'test_chrono_vault_no_logging'
if echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.address == "module.test_chrono_vault_no_logging.aws_s3_bucket_logging.chrono_vault_logging[0]")' > /dev/null; then
  echo "FAIL: Access logging resource unexpectedly created for test_chrono_vault_no_logging."
  exit 1
fi
echo "PASS: Access logging resource NOT created for test_chrono_vault_no_logging."

echo "All Terraform plan assertions passed!"
