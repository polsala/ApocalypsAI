#!/bin/bash
set -e

# Navigate to the directory containing the test configuration
cd "$(dirname "$0")"

echo "Initializing Terraform..."
# Initialize Terraform without a backend for offline testing
terraform init -backend=false

echo "Validating Terraform configuration..."
# Validate the Terraform configuration syntax
terraform validate

echo "Generating Terraform plan..."
# Generate a Terraform plan and save it to a file
terraform plan -out=tfplan

echo "Inspecting Terraform plan for expected resources..."
# Convert the plan to JSON for easier parsing and assertion
terraform show -json tfplan > tfplan.json

# Assertions: Check if key resources are present in the plan
# Mock rationale: These tests are offline and deterministic. They validate the Terraform syntax,
# configuration, and ensure that the expected AWS resources would be created without actually
# provisioning them. The 'grep' commands act as basic assertions on the generated plan,
# ensuring the core resources are present.

# Check for aws_lambda_function
grep -q "aws_lambda_function" tfplan.json
if [ $? -ne 0 ]; then
  echo "Error: aws_lambda_function not found in the plan."
  exit 1
fi

# Check for aws_s3_bucket (at least one, ideally two for code and data)
grep -q "aws_s3_bucket" tfplan.json
if [ $? -ne 0 ]; then
  echo "Error: aws_s3_bucket not found in the plan."
  exit 1
fi

# Check for aws_iam_role
grep -q "aws_iam_role" tfplan.json
if [ $? -ne 0 ]; then
  echo "Error: aws_iam_role not found in the plan."
  exit 1
fi

# Check for aws_cloudwatch_event_rule
grep -q "aws_cloudwatch_event_rule" tfplan.json
if [ $? -ne 0 ]; then
  echo "Error: aws_cloudwatch_event_rule not found in the plan."
  exit 1
fi

# Clean up generated plan files
rm tfplan tfplan.json

echo "Terraform module validation and plan generation successful! All expected resources found."
