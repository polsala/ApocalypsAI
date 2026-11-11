#!/bin/bash
set -euo pipefail

# Mock rationale: This test uses 'terraform plan -json' to generate a deployment plan
# without actually interacting with AWS. The 'jq' commands then parse this local JSON
# output to assert the presence and configuration of expected resources.
# This ensures determinism and offline execution.

echo "Running Terraform plan for test module..."

# Initialize Terraform (downloads providers, etc.)
terraform -chdir=tests init -backend=false > /dev/null

# Generate a plan in JSON format
PLAN_OUTPUT=$(terraform -chdir=tests plan -out=tfplan -json)

# Check for specific resources in the plan
echo "Verifying resource creation..."

# Check for aws_lambda_function
if ! echo "$PLAN_OUTPUT" | jq -e '.resource_changes[] | select(.type == "aws_lambda_function" and .change.actions[] == "create")' > /dev/null; then
  echo "Test failed: aws_lambda_function not found in plan or not marked for creation."
  exit 1
fi
echo "  - aws_lambda_function found and marked for creation."

# Check for aws_cloudwatch_event_rule
if ! echo "$PLAN_OUTPUT" | jq -e '.resource_changes[] | select(.type == "aws_cloudwatch_event_rule" and .change.actions[] == "create")' > /dev/null; then
  echo "Test failed: aws_cloudwatch_event_rule not found in plan or not marked for creation."
  exit 1
fi
echo "  - aws_cloudwatch_event_rule found and marked for creation."

# Check for aws_s3_bucket
if ! echo "$PLAN_OUTPUT" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.actions[] == "create")' > /dev/null; then
  echo "Test failed: aws_s3_bucket not found in plan or not marked for creation."
  exit 1
fi
echo "  - aws_s3_bucket found and marked for creation."

# Check for aws_iam_role
if ! echo "$PLAN_OUTPUT" | jq -e '.resource_changes[] | select(.type == "aws_iam_role" and .change.actions[] == "create")' > /dev/null; then
  echo "Test failed: aws_iam_role not found in plan or not marked for creation."
  exit 1
}
echo "  - aws_iam_role found and marked for creation."

# Check for specific output values (optional, but good for module testing)
LAMBDA_NAME=$(echo "$PLAN_OUTPUT" | jq -r '.resource_changes[] | select(.type == "aws_lambda_function" and .change.actions[] == "create") | .change.after.function_name')
if [[ "$LAMBDA_NAME" != "test-apocalypsai-temporal-rift-monitor" ]]; then
  echo "Test failed: Lambda function name mismatch. Expected 'test-apocalypsai-temporal-rift-monitor', got '$LAMBDA_NAME'."
  exit 1
}
echo "  - Lambda function name matches expected: $LAMBDA_NAME"

EVENT_RULE_NAME=$(echo "$PLAN_OUTPUT" | jq -r '.resource_changes[] | select(.type == "aws_cloudwatch_event_rule" and .change.actions[] == "create") | .change.after.name')
if [[ "$EVENT_RULE_NAME" != "test-apocalypsai-temporal-rift-monitor-schedule" ]]; then
  echo "Test failed: CloudWatch Event Rule name mismatch. Expected 'test-apocalypsai-temporal-rift-monitor-schedule', got '$EVENT_RULE_NAME'."
  exit 1
}
echo "  - CloudWatch Event Rule name matches expected: $EVENT_RULE_NAME"

echo "All Terraform plan checks passed successfully!"

# Clean up generated plan file
rm tfplan
