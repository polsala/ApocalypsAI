#!/bin/bash
set -euo pipefail

# Mock rationale: This test uses 'terraform plan' and 'terraform show -json' to inspect
# the generated execution plan. It does not interact with actual AWS services,
# making it deterministic and offline. 'jq' is used to parse the JSON plan output
# and assert the presence and properties of resources, effectively mocking the
# AWS environment by verifying the *intended* infrastructure state.

echo "Running Terraform module tests..."

# Ensure jq is installed
if ! command -v jq &> /dev/null
then
    echo "jq could not be found. Please install jq to run these tests (e.g., sudo apt-get install jq or brew install jq)."
    exit 1
fi

# Initialize Terraform in the test directory
terraform -chdir=tests init -backend=false

# Generate a plan and save it as JSON
terraform -chdir=tests plan -out=tfplan.out
terraform -chdir=tests show -json tfplan.out > tests/tfplan.json

# --- Assertions ---

# 1. Check if an S3 bucket resource is planned
echo "Checking for S3 bucket..."
if ! jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.actions[] == "create")' tests/tfplan.json > /dev/null; then
  echo "Test Failed: aws_s3_bucket resource not found in plan."
  exit 1
fi
echo "S3 bucket found."

# 2. Check if a Lambda function resource is planned
echo "Checking for Lambda function..."
if ! jq -e '.resource_changes[] | select(.type == "aws_lambda_function" and .change.actions[] == "create")' tests/tfplan.json > /dev/null; then
  echo "Test Failed: aws_lambda_function resource not found in plan."
  exit 1
fi
echo "Lambda function found."

# 3. Check if the S3 bucket has the correct tag
echo "Checking S3 bucket tags..."
if ! jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.after.tags.Purpose == "TemporalAnomalyBeacon")' tests/tfplan.json > /dev/null; then
  echo "Test Failed: S3 bucket does not have 'Purpose: TemporalAnomalyBeacon' tag."
  exit 1
fi
echo "S3 bucket tags verified."

# 4. Check if the Lambda function name contains the beacon_name prefix
echo "Checking Lambda function name..."
if ! jq -e '.resource_changes[] | select(.type == "aws_lambda_function" and .change.after.function_name | contains("test-chronal-rift"))' tests/tfplan.json > /dev/null; then
  echo "Test Failed: Lambda function name does not contain 'test-chronal-rift'."
  exit 1
fi
echo "Lambda function name verified."

# 5. Check if the Lambda function runtime is python3.9
echo "Checking Lambda function runtime..."
if ! jq -e '.resource_changes[] | select(.type == "aws_lambda_function" and .change.after.runtime == "python3.9")' tests/tfplan.json > /dev/null; then
  echo "Test Failed: Lambda function runtime is not 'python3.9'."
  exit 1
fi
echo "Lambda function runtime verified."

# 6. Check if the Lambda function has the LOG_LEVEL environment variable set to DEBUG
echo "Checking Lambda function environment variables..."
if ! jq -e '.resource_changes[] | select(.type == "aws_lambda_function" and .change.after.environment.variables.LOG_LEVEL == "DEBUG")' tests/tfplan.json > /dev/null; then
  echo "Test Failed: Lambda function LOG_LEVEL environment variable is not 'DEBUG'."
  exit 1
fi
echo "Lambda function environment variables verified."

echo "All Terraform module tests passed successfully!"

# Clean up generated plan files
rm tests/tfplan.out tests/tfplan.json
