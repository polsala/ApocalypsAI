#!/bin/bash

set -euo pipefail

# Mock rationale: This test script uses `terraform plan` to verify the module's configuration 
# without actually provisioning any AWS resources. The `terraform plan` output is deterministic 
# and does not require live AWS credentials, making it an offline test. 
# We are asserting that the plan contains the expected resource configurations.

TEST_DIR="$(dirname "$0")"
cd "$TEST_DIR"

echo "Initializing Terraform..."
terraform init -backend=false > /dev/null

echo "Running terraform plan..."
PLAN_OUTPUT=$(terraform plan -out=tfplan -no-color)

# Check for expected bucket name
if ! echo "$PLAN_OUTPUT" | grep -q "bucket = \"test-apocalypsai-temporal-vault-12345\""; then
  echo "Test Failed: Bucket name not found or incorrect."
  exit 1
fi

# Check for versioning enabled
if ! echo "$PLAN_OUTPUT" | grep -q "status = \"Enabled\""; then
  echo "Test Failed: Versioning not enabled."
  exit 1
fi

# Check for public access block
if ! echo "$PLAN_OUTPUT" | grep -q "block_public_acls = true" || \
   ! echo "$PLAN_OUTPUT" | grep -q "block_public_policy = true" || \
   ! echo "$PLAN_OUTPUT" | grep -q "ignore_public_acls = true" || \
   ! echo "$PLAN_OUTPUT" | grep -q "restrict_public_buckets = true"; then
  echo "Test Failed: Public access block not fully configured."
  exit 1
fi

# Check for lifecycle rule transitions to GLACIER
if ! echo "$PLAN_OUTPUT" | grep -q "storage_class = \"GLACIER\""; then
  echo "Test Failed: Lifecycle rule for GLACIER transition not found."
  exit 1
fi

# Check for specific retention days (using a more robust check with jq on json plan)
JSON_PLAN=$(terraform show -json tfplan)

# Check standard retention days
if ! echo "$JSON_PLAN" | jq -e '.resource_changes[] | select(.address == "aws_s3_bucket_lifecycle_configuration.vault_lifecycle") | .change.after.rule[0].transition[0].days == 7' > /dev/null; then
  echo "Test Failed: Standard retention days (7) not found in lifecycle transition."
  exit 1
fi

# Check glacier expiration days
if ! echo "$JSON_PLAN" | jq -e '.resource_changes[] | select(.address == "aws_s3_bucket_lifecycle_configuration.vault_lifecycle") | .change.after.rule[0].expiration[0].days == 90' > /dev/null; then
  echo "Test Failed: Glacier expiration days (90) not found in lifecycle expiration."
  exit 1
fi

# Clean up generated plan file
rm tfplan

echo "All tests passed successfully!"
