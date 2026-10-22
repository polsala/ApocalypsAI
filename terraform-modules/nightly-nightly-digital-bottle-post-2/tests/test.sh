#!/bin/bash

set -euo pipefail

echo "Running Terraform module tests..."

# Initialize Terraform in the test directory
echo "Initializing Terraform..."
terraform -chdir=./tests init -backend=false > /dev/null
# Mock rationale: -backend=false ensures no remote state or actual backend configuration
# is attempted, making the init purely local and deterministic for module parsing.
# Output is redirected to /dev/null to keep test output clean.

# Generate a plan and capture its JSON output
echo "Generating Terraform plan..."
PLAN_OUTPUT=$(terraform -chdir=./tests plan -no-color -input=false -out=tfplan)
# Mock rationale: -no-color ensures consistent output for parsing.
# -input=false prevents interactive prompts.
# -out=tfplan saves the plan for detailed inspection with 'terraform show -json'.
# This step simulates a real plan without applying, making it offline and deterministic.

JSON_PLAN=$(terraform -chdir=./tests show -json tfplan)
# Mock rationale: 'terraform show -json' provides a structured, machine-readable
# representation of the plan, which is ideal for deterministic assertions.

echo "Analyzing plan output..."

# Test Case 1: Private bucket configuration
echo "  - Verifying 'test_bottle_post_private' (private bucket)..."
# Check for aws_s3_bucket resource
if ! echo "${JSON_PLAN}" | jq -e '.resource_changes[] | select(.address == "module.test_bottle_post_private.aws_s3_bucket.bottle_post_bucket")' > /dev/null; then
  echo "FAIL: aws_s3_bucket.bottle_post_bucket not found for private module."
  exit 1
fi
# Check for private ACL
if ! echo "${JSON_PLAN}" | jq -e '.resource_changes[] | select(.address == "module.test_bottle_post_private.aws_s3_bucket.bottle_post_bucket") | .change.after.acl == "private"' > /dev/null; then
  echo "FAIL: Private bucket ACL is not 'private'."
  exit 1
fi
# Check for lifecycle rule expiration days
if ! echo "${JSON_PLAN}" | jq -e '.resource_changes[] | select(.address == "module.test_bottle_post_private.aws_s3_bucket_lifecycle_configuration.bottle_post_lifecycle") | .change.after.rule[0].expiration[0].days == 14' > /dev/null; then
  echo "FAIL: Private bucket lifecycle rule days not 14."
  exit 1
fi
# Check that aws_s3_bucket_policy is NOT created
if echo "${JSON_PLAN}" | jq -e '.resource_changes[] | select(.address == "module.test_bottle_post_private.aws_s3_bucket_policy.bottle_post_policy[0]")' > /dev/null; then
  echo "FAIL: aws_s3_bucket_policy was created for private module."
  exit 1
fi
echo "    Private bucket checks passed."

# Test Case 2: Public bucket configuration
echo "  - Verifying 'test_bottle_post_public' (public bucket)..."
# Check for aws_s3_bucket resource
if ! echo "${JSON_PLAN}" | jq -e '.resource_changes[] | select(.address == "module.test_bottle_post_public.aws_s3_bucket.bottle_post_bucket")' > /dev/null; then
  echo "FAIL: aws_s3_bucket.bottle_post_bucket not found for public module."
  exit 1
fi
# Check for public-read ACL
if ! echo "${JSON_PLAN}" | jq -e '.resource_changes[] | select(.address == "module.test_bottle_post_public.aws_s3_bucket.bottle_post_bucket") | .change.after.acl == "public-read"' > /dev/null; then
  echo "FAIL: Public bucket ACL is not 'public-read'."
  exit 1
fi
# Check for lifecycle rule expiration days
if ! echo "${JSON_PLAN}" | jq -e '.resource_changes[] | select(.address == "module.test_bottle_post_public.aws_s3_bucket_lifecycle_configuration.bottle_post_lifecycle") | .change.after.rule[0].expiration[0].days == 7' > /dev/null; then
  echo "FAIL: Public bucket lifecycle rule days not 7."
  exit 1
fi
# Check that aws_s3_bucket_policy IS created
if ! echo "${JSON_PLAN}" | jq -e '.resource_changes[] | select(.address == "module.test_bottle_post_public.aws_s3_bucket_policy.bottle_post_policy[0]")' > /dev/null; then
  echo "FAIL: aws_s3_bucket_policy was NOT created for public module."
  exit 1
fi
echo "    Public bucket checks passed."

# Test Case 3: No versioning configuration
echo "  - Verifying 'test_bottle_post_no_versioning' (no versioning)..."
# Check for aws_s3_bucket_versioning status
if ! echo "${JSON_PLAN}" | jq -e '.resource_changes[] | select(.address == "module.test_bottle_post_no_versioning.aws_s3_bucket_versioning.bottle_post_versioning") | .change.after.versioning_configuration[0].status == "Suspended"' > /dev/null; then
  echo "FAIL: No versioning bucket status is not 'Suspended'."
  exit 1
fi
echo "    No versioning checks passed."

echo "All Terraform module tests passed successfully!"

# Clean up generated plan file
rm tfplan

exit 0
