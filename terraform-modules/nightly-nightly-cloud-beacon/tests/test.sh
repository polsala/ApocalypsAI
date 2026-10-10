#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests..."

# Initialize Terraform in the test directory
terraform -chdir=tests init -backend=false -input=false

# Run terraform plan and capture output as JSON
PLAN_OUTPUT=$(terraform -chdir=tests plan -input=false -no-color -json)

# Mock rationale: We are using 'terraform plan -json' to inspect the planned changes
# without actually provisioning any cloud resources. This makes the test deterministic
# and offline. We assert on the structure and expected properties of the planned resources.
# 'jq' is used to parse the JSON output, which is a common tool for shell scripting
# with JSON data.

# Check if the plan was successful (exit code 0)
if [ $? -ne 0 ]; then
  echo "Terraform plan failed!"
  echo "$PLAN_OUTPUT"
  exit 1
fi

echo "Terraform plan successful. Analyzing output..."

# Assert that an S3 bucket is planned
if ! echo "$PLAN_OUTPUT" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.actions[] == "create")' > /dev/null; then
  echo "Test failed: aws_s3_bucket resource not found in plan."
  exit 1
fi

# Assert that S3 bucket website configuration is planned
if ! echo "$PLAN_OUTPUT" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_website_configuration" and .change.actions[] == "create")' > /dev/null; then
  echo "Test failed: aws_s3_bucket_website_configuration resource not found in plan."
  exit 1
fi

# Assert that S3 bucket policy is planned
if ! echo "$PLAN_OUTPUT" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_policy" and .change.actions[] == "create")' > /dev/null; then
  echo "Test failed: aws_s3_bucket_policy resource not found in plan."
  exit 1
fi

# Assert that S3 bucket object (index.html) is planned
if ! echo "$PLAN_OUTPUT" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_object" and .change.actions[] == "create" and .change.after.key == "index.html")' > /dev/null; then
  echo "Test failed: aws_s3_bucket_object for index.html not found in plan."
  exit 1
fi

# Assert that the output `test_website_endpoint` is present in the plan
if ! echo "$PLAN_OUTPUT" | jq -e '.outputs.test_website_endpoint' > /dev/null; then
  echo "Test failed: Output 'test_website_endpoint' not found in plan."
  exit 1
fi

# Assert that the output `test_bucket_name` is present in the plan
if ! echo "$PLAN_OUTPUT" | jq -e '.outputs.test_bucket_name' > /dev/null; then
  echo "Test failed: Output 'test_bucket_name' not found in plan."
  exit 1
fi

echo "All Terraform plan assertions passed!"
