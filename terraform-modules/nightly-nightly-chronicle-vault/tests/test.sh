#!/bin/bash

set -euo pipefail

# Mock rationale: This script runs 'terraform plan' in a test directory.
# 'terraform plan' is an offline operation that generates an execution plan
# without interacting with the actual cloud provider. We then parse its output
# to assert that the module would create resources with the expected properties.
# This makes the test deterministic and offline.

TEST_DIR="tests"
MODULE_SRC="../src"

echo "Initializing Terraform in ${TEST_DIR}..."
terraform -chdir="${TEST_DIR}" init -backend=false -input=false > /dev/null

echo "Running terraform plan and capturing output..."
PLAN_OUTPUT=$(terraform -chdir="${TEST_DIR}" plan -no-color -input=false -out=tfplan)

echo "Verifying S3 bucket creation..."
if ! echo "${PLAN_OUTPUT}" | grep -q 'resource "aws_s3_bucket" "chronicle_vault"'; then
  echo "Test Failed: S3 bucket resource not found in plan."
  exit 1
fi

echo "Verifying bucket name prefix..."
if ! echo "${PLAN_OUTPUT}" | grep -q 'bucket: "test-apocalypsai-vault-'; then
  echo "Test Failed: Expected bucket name prefix 'test-apocalypsai-vault-' not found."
  exit 1
fi

echo "Verifying versioning is enabled..."
if ! echo "${PLAN_OUTPUT}" | grep -q 'versioning_configuration.0.status: "Enabled"'; then
  echo "Test Failed: Versioning not enabled."
  exit 1
fi

echo "Verifying server-side encryption (SSE-S3) is enabled..."
if ! echo "${PLAN_OUTPUT}" | grep -q 'apply_server_side_encryption_by_default.0.sse_algorithm: "AES256"'; then
  echo "Test Failed: SSE-S3 not enabled."
  exit 1
}

echo "Verifying public access block is enabled..."
if ! echo "${PLAN_OUTPUT}" | grep -q 'block_public_acls: true'; then
  echo "Test Failed: Public ACLs not blocked."
  exit 1
fi
if ! echo "${PLAN_OUTPUT}" | grep -q 'block_public_policy: true'; then
  echo "Test Failed: Public policy not blocked."
  exit 1
fi

echo "Verifying lifecycle rule for Glacier Deep Archive transition..."
if ! echo "${PLAN_OUTPUT}" | grep -q 'noncurrent_version_transition.0.days: 90'; then
  echo "Test Failed: Glacier transition days not set to 90."
  exit 1
fi
if ! echo "${PLAN_OUTPUT}" | grep -q 'noncurrent_version_transition.0.storage_class: "DEEP_ARCHIVE"'; then
  echo "Test Failed: Storage class not set to DEEP_ARCHIVE."
  exit 1
fi

echo "Verifying lifecycle rule for incomplete multipart uploads expiration..."
if ! echo "${PLAN_OUTPUT}" | grep -q 'abort_incomplete_multipart_upload_days: 3'; then
  echo "Test Failed: Incomplete multipart upload expiration days not set to 3."
  exit 1
fi

echo "Verifying tags..."
if ! echo "${PLAN_OUTPUT}" | grep -q 'tags.Module: "ChronicleVault"'; then
  echo "Test Failed: Tag 'Module' not found or incorrect."
  exit 1
fi
if ! echo "${PLAN_OUTPUT}" | grep -q 'tags.TestEnv: "True"'; then
  echo "Test Failed: Tag 'TestEnv' not found or incorrect."
  exit 1
fi

echo "All Terraform plan checks passed successfully!"

# Clean up the generated plan file
rm "${TEST_DIR}/tfplan"
rm -rf "${TEST_DIR}/.terraform"
rm "${TEST_DIR}/.terraform.lock.hcl"
