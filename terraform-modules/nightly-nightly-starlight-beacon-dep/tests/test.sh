#!/bin/bash

set -euo pipefail

echo "Running Starlight Beacon Deployer module tests..."

# Initialize Terraform in the test directory
# Mock rationale: -backend=false prevents Terraform from trying to configure a state backend,
# making the test fully offline and deterministic.
terraform init -backend=false

# Generate a plan without applying it
# Mock rationale: -no-color for easier parsing, -out=tfplan to save the plan for inspection.
# This command does not interact with AWS API.
terraform plan -no-color -out=tfplan

# Show the plan in JSON format for programmatic inspection
PLAN_JSON=$(terraform show -json tfplan)

# --- Assertions ---

# Check for the creation of aws_s3_bucket
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.actions[] == "create")' > /dev/null; then
  echo "Test Failed: aws_s3_bucket resource not found in plan or not marked for creation."
  exit 1
fi
echo "PASS: aws_s3_bucket resource found and marked for creation."

# Check for the creation of aws_s3_bucket_policy
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_policy" and .change.actions[] == "create")' > /dev/null; then
  echo "Test Failed: aws_s3_bucket_policy resource not found in plan or not marked for creation."
  exit 1
fi
echo "PASS: aws_s3_bucket_policy resource found and marked for creation."

# Check for the creation of aws_s3_bucket_object (index.html)
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_object" and .change.actions[] == "create" and .change.after.key == "index.html")' > /dev/null; then
  echo "Test Failed: aws_s3_bucket_object for index.html not found in plan or not marked for creation."
  exit 1
fi
echo "PASS: aws_s3_bucket_object (index.html) resource found and marked for creation."

# Check for the creation of aws_cloudfront_distribution
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_cloudfront_distribution" and .change.actions[] == "create")' > /dev/null; then
  echo "Test Failed: aws_cloudfront_distribution resource not found in plan or not marked for creation."
  exit 1
fi
echo "PASS: aws_cloudfront_distribution resource found and marked for creation."

# Check for expected outputs
if ! echo "$PLAN_JSON" | jq -e '.configuration.outputs.test_cloudfront_domain_name' > /dev/null; then
  echo "Test Failed: 'test_cloudfront_domain_name' output not found in plan."
  exit 1
fi
echo "PASS: 'test_cloudfront_domain_name' output found."

if ! echo "$PLAN_JSON" | jq -e '.configuration.outputs.test_s3_bucket_name' > /dev/null; then
  echo "Test Failed: 'test_s3_bucket_name' output not found in plan."
  exit 1
fi
echo "PASS: 'test_s3_bucket_name' output found."

# Clean up the plan file
rm tfplan

echo "All tests passed successfully!"
