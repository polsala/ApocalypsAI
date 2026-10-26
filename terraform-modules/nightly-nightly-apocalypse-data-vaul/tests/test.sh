#!/bin/bash

set -euo pipefail

# Mock rationale: Terraform init downloads providers but does not require AWS credentials for basic validation.
# Terraform validate checks HCL syntax offline. Terraform plan generates an execution plan without applying it.
# We use dummy ARNs for replication to ensure the configuration is valid without needing real resources.

TEST_DIR="$(mktemp -d)"
MODULE_PATH="$(dirname "$0")"/../src
FIXTURE_PATH="$(dirname "$0")"/fixtures

echo "Running tests in: ${TEST_DIR}"

cleanup() {
  echo "Cleaning up ${TEST_DIR}"
  rm -rf "${TEST_DIR}"
}

trap cleanup EXIT

# --- Test Case 1: Basic Vault (no replication, no glacier) ---

echo "\n--- Running Basic Vault Test ---"
rm -rf "${TEST_DIR}"/* # Ensure clean slate for first test
cp "${FIXTURE_PATH}/basic_vault.tf" "${TEST_DIR}/main.tf"
mkdir -p "${TEST_DIR}/modules/apocalypse-vault"
cp "${MODULE_PATH}"/* "${TEST_DIR}/modules/apocalypse-vault/"

cd "${TEST_DIR}"

terraform init -backend=false -input=false
if [ $? -ne 0 ]; then
  echo "ERROR: Terraform init failed for basic vault."
  exit 1
fi

terraform validate
if [ $? -ne 0 ]; then
  echo "ERROR: Terraform validate failed for basic vault."
  exit 1
fi

# terraform plan should show changes (exit code 2) for a new plan
terraform plan -detailed-exitcode -out=tfplan -var="bucket_name_prefix=test-basic" -var="region=us-east-1"
if [ $? -ne 2 ]; then
  echo "ERROR: Terraform plan did not indicate pending changes (exit code 2) for basic vault."
  exit 1
fi

# Verify key resources/properties in the plan
PLAN_JSON=$(terraform show -json tfplan)

if ! echo "${PLAN_JSON}" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket") | .change.actions[] | contains("create")' > /dev/null; then
  echo "ERROR: aws_s3_bucket not found in plan for basic vault."
  exit 1
fi

if ! echo "${PLAN_JSON}" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_versioning") | .change.actions[] | contains("create")' > /dev/null; then
  echo "ERROR: aws_s3_bucket_versioning not found in plan for basic vault."
  exit 1
fi

if ! echo "${PLAN_JSON}" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_server_side_encryption_configuration") | .change.actions[] | contains("create")' > /dev/null; then
  echo "ERROR: aws_s3_bucket_server_side_encryption_configuration not found in plan for basic vault."
  exit 1
fi

echo "Basic Vault Test PASSED."

# --- Test Case 2: Vault with Replication and Glacier ---

echo "\n--- Running Replication and Glacier Vault Test ---"
rm -rf "${TEST_DIR}"/* # Clear previous test files
cp "${FIXTURE_PATH}/replication_glacier_vault.tf" "${TEST_DIR}/main.tf"
mkdir -p "${TEST_DIR}/modules/apocalypse-vault"
cp "${MODULE_PATH}"/* "${TEST_DIR}/modules/apocalypse-vault/"

cd "${TEST_DIR}"

terraform init -backend=false -input=false
if [ $? -ne 0 ]; then
  echo "ERROR: Terraform init failed for replication/glacier vault."
  exit 1
fi

terraform validate
if [ $? -ne 0 ]; then
  echo "ERROR: Terraform validate failed for replication/glacier vault."
  exit 1
fi

terraform plan -detailed-exitcode -out=tfplan \
  -var="bucket_name_prefix=test-repl-glacier" \
  -var="region=us-east-1" \
  -var="enable_replication=true" \
  -var="replication_destination_bucket_arn=arn:aws:s3:::mock-replication-target" \
  -var="enable_glacier_archive=true" \
  -var="glacier_transition_days=60"

if [ $? -ne 2 ]; then
  echo "ERROR: Terraform plan did not indicate pending changes (exit code 2) for replication/glacier vault."
  exit 1
fi

PLAN_JSON=$(terraform show -json tfplan)

if ! echo "${PLAN_JSON}" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_replication_configuration") | .change.actions[] | contains("create")' > /dev/null; then
  echo "ERROR: aws_s3_bucket_replication_configuration not found in plan."
  exit 1
fi

if ! echo "${PLAN_JSON}" | jq -e '.resource_changes[] | select(.type == "aws_iam_role") | .change.actions[] | contains("create")' > /dev/null; then
  echo "ERROR: aws_iam_role for replication not found in plan."
  exit 1
fi

if ! echo "${PLAN_JSON}" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_lifecycle_configuration") | .change.actions[] | contains("create")' > /dev/null; then
  echo "ERROR: aws_s3_bucket_lifecycle_configuration not found in plan."
  exit 1
fi

echo "Replication and Glacier Vault Test PASSED."

echo "\nAll tests PASSED!"
