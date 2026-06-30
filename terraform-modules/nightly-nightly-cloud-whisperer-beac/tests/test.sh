#!/bin/bash

set -euo pipefail

echo "--- Running Terraform tests for Nightly Cloud-Whisperer Beacon ---"

# Mock rationale: Terraform plan and validate are offline operations.
# We are testing the module's syntax, variable handling, and expected resource definitions
# without actually provisioning cloud resources. This ensures the module is well-formed
# and produces a predictable plan.

# Initialize Terraform in the test directory
echo "Initializing Terraform..."
terraform -chdir=tests init -backend=false > /dev/null

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform -chdir=tests validate

if [ $? -ne 0 ]; then
  echo "Terraform validation failed!"
  exit 1
fi
echo "Terraform configuration is valid."

# Generate a plan and output it as JSON
echo "Generating Terraform plan..."
terraform -chdir=tests plan -out=tfplan -input=false -var="bucket_name_prefix=test-apocalypsai-whisper" -var="region=us-east-1" -var="initial_whisper_message=Test whisper: The code compiles, for now."

if [ $? -ne 0 ]; then
  echo "Terraform plan generation failed!"
  exit 1
fi

# Show the plan in JSON format and parse it
PLAN_JSON=$(terraform -chdir=tests show -json tfplan)

# Assertions
echo "Performing assertions on the plan..."

# Check for the S3 bucket resource
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.actions[] == "create")' > /dev/null; then
  echo "Assertion failed: aws_s3_bucket resource not found in plan."
  exit 1
fi
echo "Assertion passed: aws_s3_bucket resource found."

# Check for the S3 bucket policy resource
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_policy" and .change.actions[] == "create")' > /dev/null; then
  echo "Assertion failed: aws_s3_bucket_policy resource not found in plan."
  exit 1
fi
echo "Assertion passed: aws_s3_bucket_policy resource found."

# Check for index.html object
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_object" and .name == "index_html" and .change.actions[] == "create")' > /dev/null; then
  echo "Assertion failed: aws_s3_bucket_object (index_html) resource not found in plan."
  exit 1
fi
echo "Assertion passed: aws_s3_bucket_object (index_html) resource found."

# Check for error.html object
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_object" and .name == "error_html" and .change.actions[] == "create")' > /dev/null; then
  echo "Assertion failed: aws_s3_bucket_object (error_html) resource not found in plan."
  exit 1
fi
echo "Assertion passed: aws_s3_bucket_object (error_html) resource found."

# Check if the bucket name prefix is used in the planned bucket name
# This requires parsing the 'after' attribute of the bucket resource
BUCKET_NAME_PLANNED=$(echo "$PLAN_JSON" | jq -r '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.actions[] == "create") | .change.after.bucket')
if [[ "$BUCKET_NAME_PLANNED" != "test-apocalypsai-whisper-"* ]]; then
  echo "Assertion failed: Planned bucket name '$BUCKET_NAME_PLANNED' does not start with 'test-apocalypsai-whisper-'."
  exit 1
fi
echo "Assertion passed: Planned bucket name starts with the correct prefix."

# Check if the website configuration is present
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.actions[] == "create" and .change.after.website.index_document == "index.html")' > /dev/null; then
  echo "Assertion failed: S3 bucket website configuration (index_document) not found or incorrect."
  exit 1
fi
echo "Assertion passed: S3 bucket website configuration (index_document) found."

echo "All Terraform tests passed successfully!"

# Clean up the plan file
rm tfplan
