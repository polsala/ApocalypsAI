#!/bin/bash
set -euo pipefail

TEST_DIR="$(dirname "$0")"
MODULE_DIR="${TEST_DIR}/../src"

echo "--- Running Terraform tests for Whisperwind Message Relay ---"

# Mock rationale: terraform init downloads providers. For offline testing,
# we assume providers are cached after the first run.
# This step is essential for subsequent validate/plan commands.
echo "1. Initializing Terraform in test directory..."
terraform -chdir="${TEST_DIR}" init -backend=false -upgrade > /dev/null

echo "2. Validating Terraform configuration..."
terraform -chdir="${TEST_DIR}" validate

echo "3. Planning Terraform changes (expecting 4 resources to add)..."
PLAN_OUTPUT=$(terraform -chdir="${TEST_DIR}" plan -no-color -detailed-exitcode)
PLAN_EXIT_CODE=$?

# detailed-exitcode:
# 0 = Succeeded with no diffs
# 1 = Error
# 2 = Succeeded with diffs

if [ "$PLAN_EXIT_CODE" -eq 2 ]; then
  echo "Terraform plan indicates changes will be made (as expected for new resources)."
  # Check for specific resources in the plan output
  if echo "$PLAN_OUTPUT" | grep -q "aws_sqs_queue.whisperwind_queue"; then
    echo "  - Found aws_sqs_queue.whisperwind_queue in plan."
  else
    echo "Error: aws_sqs_queue.whisperwind_queue not found in plan."
    exit 1
  fi
  if echo "$PLAN_OUTPUT" | grep -q "aws_sns_topic.whisperwind_topic"; then
    echo "  - Found aws_sns_topic.whisperwind_topic in plan."
  else
    echo "Error: aws_sns_topic.whisperwind_topic not found in plan."
    exit 1
  fi
  if echo "$PLAN_OUTPUT" | grep -q "aws_sns_topic_subscription.whisperwind_subscription"; then
    echo "  - Found aws_sns_topic_subscription.whisperwind_subscription in plan."
  else
    echo "Error: aws_sns_topic_subscription.whisperwind_subscription not found in plan."
    exit 1
  fi
  if echo "$PLAN_OUTPUT" | grep -q "aws_sqs_queue_policy.whisperwind_queue_policy"; then
    echo "  - Found aws_sqs_queue_policy.whisperwind_queue_policy in plan."
  else
    echo "Error: aws_sqs_queue_policy.whisperwind_queue_policy not found in plan."
    exit 1
  fi

  # Check for the summary line "Plan: 4 to add, 0 to change, 0 to destroy."
  if echo "$PLAN_OUTPUT" | grep -q "Plan: 4 to add, 0 to change, 0 to destroy."; then
    echo "  - Plan summary matches expected: 4 resources to add."
  else
    echo "Error: Plan summary does not match expected '4 to add'."
    echo "$PLAN_OUTPUT"
    exit 1
  fi

else
  echo "Error: Terraform plan did not indicate changes or failed. Exit code: $PLAN_EXIT_CODE"
  echo "$PLAN_OUTPUT"
  exit 1
fi

echo "All Terraform tests passed successfully!"
