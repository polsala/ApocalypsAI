#!/bin/bash

set -euo pipefail

echo "Running Terraform module tests..."

# Navigate to the test directory
cd "$(dirname "$0")"

# Clean up previous runs
rm -rf .terraform .terraform.lock.hcl terraform.tfstate* lambda_function_payload.zip || true

echo "Initializing Terraform..."
terraform init -backend=false # Mock rationale: No actual backend needed for plan/validate

echo "Validating Terraform configuration..."
terraform validate

echo "Generating Terraform plan (dry run)..."
terraform plan -out=tfplan -input=false -var="prefix=test-apocalypsai-hunt" -var="region=us-east-1" -var="instance_type=t2.micro" -var="lambda_runtime=nodejs18.x"

# Check if the plan file was created
if [ ! -f tfplan ]; then
  echo "Error: Terraform plan file 'tfplan' was not created."
  exit 1
fi

echo "Inspecting plan for expected outputs (basic check)..."
# This is a very basic check. A more robust test would parse the plan JSON.
# For this exercise, we'll just ensure the plan command itself succeeded.
# We can also check for specific resource types or tags if we want to be more thorough.
# For now, successful plan generation is the primary goal for a module test.
terraform show -json tfplan | grep "test_s3_bucket_name" > /dev/null
if [ $? -ne 0 ]; then
  echo "Error: S3 bucket output not found in plan."
  exit 1
fi

terraform show -json tfplan | grep "test_ec2_instance_id" > /dev/null
if [ $? -ne 0 ]; then
  echo "Error: EC2 instance output not found in plan."
  exit 1
fi

terraform show -json tfplan | grep "test_lambda_function_name" > /dev/null
if [ $? -ne 0 ]; then
  echo "Error: Lambda function output not found in plan."
  exit 1
fi

terraform show -json tfplan | grep "test_dynamodb_table_name" > /dev/null
if [ $? -ne 0 ]; then
  echo "Error: DynamoDB table output not found in plan."
  exit 1
fi

echo "Terraform module tests passed successfully!"

# Clean up generated plan file
rm tfplan lambda_function_payload.zip
