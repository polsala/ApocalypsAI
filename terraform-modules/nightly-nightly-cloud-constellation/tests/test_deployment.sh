#!/bin/bash
set -euo pipefail

# Mock rationale: `terraform validate` performs a static analysis of the configuration
# without needing AWS credentials or actual resource provisioning.
# It ensures the HCL syntax is correct and references are valid within the module.
echo "Running Terraform validation..."
terraform init -backend=false # Initialize without a backend for local validation
terraform validate

if [ $? -eq 0 ]; then
    echo "Terraform configuration is valid."
else
    echo "Terraform configuration validation failed."
    exit 1
fi

# Mock rationale: `terraform plan -no-color` generates an execution plan.
# We can check its output for expected resource types without actually applying.
# This is a robust offline test for resource existence and basic configuration.
echo "Checking for expected resources in plan..."
PLAN_OUTPUT=$(terraform plan -no-color -var="project_name=test-constellation" -var="aws_region=us-east-1" 2>&1)

# Check for key resources
echo "$PLAN_OUTPUT" | grep -q "aws_lambda_function.constellation_generator" || { echo "ERROR: Lambda function not found in plan."; exit 1; }
echo "$PLAN_OUTPUT" | grep -q "aws_apigatewayv2_api.http_api" || { echo "ERROR: API Gateway not found in plan."; exit 1; }
echo "$PLAN_OUTPUT" | grep -q "aws_iam_role.lambda_exec_role" || { echo "ERROR: IAM role not found in plan."; exit 1; }
echo "$PLAN_OUTPUT" | grep -q "aws_lambda_permission.api_gateway_permission" || { echo "ERROR: Lambda permission not found in plan."; exit 1; }

echo "All expected resources found in Terraform plan."

echo "Tests passed successfully!"
