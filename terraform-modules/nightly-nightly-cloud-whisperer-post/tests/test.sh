#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests..."

# Initialize Terraform in the test directory
# Mock rationale: -backend=false ensures no state is stored remotely, -no-color for consistent grep output.
terraform -chdir=tests init -backend=false -no-color

# Run terraform plan and capture output
# Mock rationale: -detailed-exitcode provides specific exit codes for plan results (0=no changes, 1=error, 2=changes).
PLAN_OUTPUT=$(terraform -chdir=tests plan -no-color -detailed-exitcode)
PLAN_EXIT_CODE=$?

if [ "$PLAN_EXIT_CODE" -eq 1 ]; then
  echo "Test failed: Terraform plan encountered an error."
  exit 1
elif [ "$PLAN_EXIT_CODE" -eq 0 ]; then
  echo "Test failed: Terraform plan reported no changes, but resources should be created by a new module."
  exit 1
fi
# If PLAN_EXIT_CODE is 2, it means there are changes, which is what we expect for a new module.

echo "Terraform plan output (expecting changes):"
echo "$PLAN_OUTPUT"

# Test 1: Check if aws_s3_bucket resource is planned for creation
if ! echo "$PLAN_OUTPUT" | grep -q 'resource "aws_s3_bucket" "postbox"'; then
  echo "Test failed: aws_s3_bucket.postbox not found in plan."
  exit 1
fi

# Test 2: Check if aws_sns_topic resource is planned for creation
if ! echo "$PLAN_OUTPUT" | grep -q 'resource "aws_sns_topic" "whisper_channel"'; then
  echo "Test failed: aws_sns_topic.whisper_channel not found in plan."
  exit 1
fi

# Test 3: Check if aws_s3_bucket_notification resource is planned for creation
if ! echo "$PLAN_OUTPUT" | grep -q 'resource "aws_s3_bucket_notification" "postbox_notifications"'; then
  echo "Test failed: aws_s3_bucket_notification.postbox_notifications not found in plan."
  exit 1
fi

# Test 4: Check if the S3 bucket notification is configured for ObjectCreated events
if ! echo "$PLAN_OUTPUT" | grep -q 'events = \[
      "s3:ObjectCreated:\*",
    \]'; then
  echo "Test failed: S3 bucket notification not configured for s3:ObjectCreated:* events."
  exit 1
fi

# Test 5: Check if the S3 bucket notification is configured with the correct SNS topic ARN
if ! echo "$PLAN_OUTPUT" | grep -q 'topic_arn = aws_sns_topic.whisper_channel.arn'; then
  echo "Test failed: S3 bucket notification 'topic_arn' not correctly linked to SNS topic."
  exit 1
fi

# Test 6: Check if the notification filter prefix is applied
if ! echo "$PLAN_OUTPUT" | grep -q 'filter_prefix = "inbox/"'; then
  echo "Test failed: Notification filter prefix 'inbox/' not found."
  exit 1
fi

# Test 7: Check if the SNS topic policy allows S3 to publish
if ! echo "$PLAN_OUTPUT" | grep -q 'principals {\n      type        = "Service"\n      identifiers = \[
        "s3.amazonaws.com",\n      \]'; then
  echo "Test failed: SNS topic policy does not allow S3 service principal to publish."
  exit 1
fi

echo "All Terraform module tests passed successfully!"
exit 0
