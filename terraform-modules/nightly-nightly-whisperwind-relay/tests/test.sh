#!/bin/bash
set -euo pipefail

echo "--- Running Terraform module tests ---"

# Navigate to the test directory
cd "$(dirname "$0")"

# Mock rationale: Terraform init needs to be run to download providers,
# but no actual cloud resources are created during 'terraform plan'.
# The 'plan -json' output is deterministic based on the HCL.
terraform init -backend=false -input=false

# Run terraform plan and capture JSON output
PLAN_JSON=$(terraform plan -json -input=false -no-color)

# Check if the SQS queue resource is planned for creation
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_sqs_queue" and .name == "whisperwind_relay" and .change.actions[] == "create")' > /dev/null; then
  echo "Test Failed: aws_sqs_queue.whisperwind_relay resource not found in plan or not marked for creation."
  exit 1
fi

echo "Passed: aws_sqs_queue.whisperwind_relay resource is planned for creation."

# Check specific attributes
RELAY_NAME=$(echo "$PLAN_JSON" | jq -r '.resource_changes[] | select(.type == "aws_sqs_queue" and .name == "whisperwind_relay").change.after.name')
if [[ "$RELAY_NAME" != "test-whisperwind-relay-alpha" ]]; then
  echo "Test Failed: Expected relay_name 'test-whisperwind-relay-alpha', got '$RELAY_NAME'."
  exit 1
fi
echo "Passed: Relay name is correct."

VISIBILITY_TIMEOUT=$(echo "$PLAN_JSON" | jq -r '.resource_changes[] | select(.type == "aws_sqs_queue" and .name == "whisperwind_relay").change.after.visibility_timeout_seconds')
if [[ "$VISIBILITY_TIMEOUT" != "60" ]]; then
  echo "Test Failed: Expected visibility_timeout_seconds '60', got '$VISIBILITY_TIMEOUT'."
  exit 1
fi
echo "Passed: Visibility timeout is correct."

MESSAGE_RETENTION=$(echo "$PLAN_JSON" | jq -r '.resource_changes[] | select(.type == "aws_sqs_queue" and .name == "whisperwind_relay").change.after.message_retention_seconds')
if [[ "$MESSAGE_RETENTION" != "86400" ]]; then
  echo "Test Failed: Expected message_retention_seconds '86400', got '$MESSAGE_RETENTION'."
  exit 1
fi
echo "Passed: Message retention is correct."

DELAY_SECONDS=$(echo "$PLAN_JSON" | jq -r '.resource_changes[] | select(.type == "aws_sqs_queue" and .name == "whisperwind_relay").change.after.delay_seconds')
if [[ "$DELAY_SECONDS" != "5" ]]; then
  echo "Test Failed: Expected delay_seconds '5', got '$DELAY_SECONDS'."
  exit 1
fi
echo "Passed: Delay seconds is correct."

echo "All Terraform module tests passed successfully!"
