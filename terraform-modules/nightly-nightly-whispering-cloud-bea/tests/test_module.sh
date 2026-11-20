#!/bin/bash
set -euo pipefail

TEST_DIR="tests/fixtures"

echo "--- Running Terraform Validation ---"
terraform -chdir="$TEST_DIR" init -backend=false # Mock rationale: -backend=false avoids state file creation and remote backend interaction.
terraform -chdir="$TEST_DIR" validate

echo "--- Running Terraform Plan and Assertions ---"
terraform -chdir="$TEST_DIR" plan -out=tfplan -no-color # Mock rationale: -no-color for easier parsing.
PLAN_JSON=$(terraform -chdir="$TEST_DIR" show -json tfplan)

# Assert that an S3 bucket resource is planned
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket")' > /dev/null; then
  echo "ERROR: aws_s3_bucket resource not found in plan."
  exit 1
fi

# Assert that an S3 bucket ACL resource is planned
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_acl")' > /dev/null; then
  echo "ERROR: aws_s3_bucket_acl resource not found in plan."
  exit 1
fi

# Assert that an S3 bucket public access block resource is planned
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_public_access_block")' > /dev/null; then
  echo "ERROR: aws_s3_bucket_public_access_block resource not found in plan."
  exit 1
fi

# Assert that an S3 bucket website configuration is planned
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_website_configuration")' > /dev/null; then
  echo "ERROR: aws_s3_bucket_website_configuration resource not found in plan."
  exit 1
fi

# Assert that an S3 bucket policy is planned
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_policy")' > /dev/null; then
  echo "ERROR: aws_s3_bucket_policy resource not found in plan."
  exit 1
}

# Assert that an S3 object (index.html) is planned
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_object" and .change.after.key == "index.html")' > /dev/null; then
  echo "ERROR: aws_s3_object for index.html not found in plan."
  exit 1
fi

# Assert that the output 'beacon_url' is present in the plan (though its value will be unknown until apply)
if ! echo "$PLAN_JSON" | jq -e '.planned_values.outputs.beacon_url' > /dev/null; then
  echo "ERROR: Output 'beacon_url' not found in plan."
  exit 1
fi

echo "All Terraform plan assertions passed successfully."

# Clean up the plan file
rm "$TEST_DIR/tfplan"

echo "Terraform module test completed successfully."
