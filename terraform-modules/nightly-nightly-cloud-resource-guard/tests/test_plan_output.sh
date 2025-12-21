#!/bin/bash
set -euo pipefail

# Mock rationale: This test runs `terraform init` and `terraform plan` in a temporary directory
# without connecting to any real cloud provider or state backend. It then parses the JSON output
# of the plan using `jq` to assert that the resources and their properties are correctly defined.
# This ensures the module's configuration is valid and as expected, deterministically and offline.

TEMP_DIR=$(mktemp -d)
echo "Running tests in temporary directory: $TEMP_DIR"
cp -r src/* "$TEMP_DIR/"

cd "$TEMP_DIR"

echo "Initializing Terraform..."
terraform init -backend=false > /dev/null # Mock rationale: Prevents connection to a real state backend.

echo "Generating Terraform plan JSON..."
PLAN_JSON=$(terraform plan -var="project_name=test" -var="environment=dev" -var="budget_threshold=5" -json) # Mock rationale: Generates a plan without applying, using mock variables.

# Assertions using jq
echo "Asserting resource counts and properties..."

# Check if plan_json is empty or invalid
if [ -z "$PLAN_JSON" ]; then
    echo "Error: Terraform plan JSON is empty."
    exit 1
fi

# Check for resource changes (create operations)
RESOURCE_CHANGES=$(echo "$PLAN_JSON" | jq '.resource_changes[] | select(.change.actions[] == "create")')
NUM_RESOURCES=$(echo "$RESOURCE_CHANGES" | jq -s 'length')

if [ "$NUM_RESOURCES" -ne 6 ]; then
    echo "Test Failed: Expected 6 resources to be created, but found $NUM_RESOURCES."
    echo "Resource changes found:"
    echo "$RESOURCE_CHANGES"
    exit 1
}

# Assert S3 Bucket properties
S3_BUCKET=$(echo "$RESOURCE_CHANGES" | jq -r 'select(.type == "aws_s3_bucket" and .name == "survival_cache")')
if [ -z "$S3_BUCKET" ]; then
    echo "Test Failed: aws_s3_bucket.survival_cache not found in plan."
    exit 1
}
echo "$S3_BUCKET" | jq -e '.change.after.bucket | contains("test-dev-survival-cache")' || { echo "Test Failed: S3 bucket name incorrect."; exit 1; }
echo "$S3_BUCKET" | jq -e '.change.after.tags.Project == "test"' || { echo "Test Failed: S3 bucket tag 'Project' incorrect."; exit 1; }
echo "$S3_BUCKET" | jq -e '.change.after.tags.Purpose == "Survival Cache"' || { echo "Test Failed: S3 bucket tag 'Purpose' incorrect."; exit 1; }

# Assert S3 Public Access Block properties
S3_PAB=$(echo "$RESOURCE_CHANGES" | jq -r 'select(.type == "aws_s3_bucket_public_access_block" and .name == "survival_cache_block")')
if [ -z "$S3_PAB" ]; then
    echo "Test Failed: aws_s3_bucket_public_access_block.survival_cache_block not found in plan."
    exit 1
}
echo "$S3_PAB" | jq -e '.change.after.block_public_acls == true' || { echo "Test Failed: S3 PAB block_public_acls incorrect."; exit 1; }
echo "$S3_PAB" | jq -e '.change.after.restrict_public_buckets == true' || { echo "Test Failed: S3 PAB restrict_public_buckets incorrect."; exit 1; }

# Assert S3 Versioning properties
S3_VERSIONING=$(echo "$RESOURCE_CHANGES" | jq -r 'select(.type == "aws_s3_bucket_versioning" and .name == "survival_cache_versioning")')
if [ -z "$S3_VERSIONING" ]; then
    echo "Test Failed: aws_s3_bucket_versioning.survival_cache_versioning not found in plan."
    exit 1
}
echo "$S3_VERSIONING" | jq -e '.change.after.versioning_configuration[0].status == "Enabled"' || { echo "Test Failed: S3 Versioning status incorrect."; exit 1; }

# Assert S3 Encryption properties
S3_ENCRYPTION=$(echo "$RESOURCE_CHANGES" | jq -r 'select(.type == "aws_s3_bucket_server_side_encryption_configuration" and .name == "survival_cache_encryption")')
if [ -z "$S3_ENCRYPTION" ]; then
    echo "Test Failed: aws_s3_bucket_server_side_encryption_configuration.survival_cache_encryption not found in plan."
    exit 1
}
echo "$S3_ENCRYPTION" | jq -e '.change.after.rule[0].apply_server_side_encryption_by_default[0].sse_algorithm == "AES256"' || { echo "Test Failed: S3 Encryption algorithm incorrect."; exit 1; }

# Assert SNS Topic properties
SNS_TOPIC=$(echo "$RESOURCE_CHANGES" | jq -r 'select(.type == "aws_sns_topic" and .name == "alert_topic")')
if [ -z "$SNS_TOPIC" ]; then
    echo "Test Failed: aws_sns_topic.alert_topic not found in plan."
    exit 1
}
echo "$SNS_TOPIC" | jq -e '.change.after.name | contains("test-dev-alert-topic")' || { echo "Test Failed: SNS topic name incorrect."; exit 1; }
echo "$SNS_TOPIC" | jq -e '.change.after.tags.Project == "test"' || { echo "Test Failed: SNS topic tag 'Project' incorrect."; exit 1; }

# Assert CloudWatch Alarm properties
CLOUDWATCH_ALARM=$(echo "$RESOURCE_CHANGES" | jq -r 'select(.type == "aws_cloudwatch_metric_alarm" and .name == "budget_alarm")')
if [ -z "$CLOUDWATCH_ALARM" ]; then
    echo "Test Failed: aws_cloudwatch_metric_alarm.budget_alarm not found in plan."
    exit 1
}
echo "$CLOUDWATCH_ALARM" | jq -e '.change.after.alarm_name | contains("test-dev-budget-alarm")' || { echo "Test Failed: CloudWatch alarm name incorrect."; exit 1; }
echo "$CLOUDWATCH_ALARM" | jq -e '.change.after.metric_name == "EstimatedCharges"' || { echo "Test Failed: CloudWatch alarm metric_name incorrect."; exit 1; }
echo "$CLOUDWATCH_ALARM" | jq -e '.change.after.namespace == "AWS/Billing"' || { echo "Test Failed: CloudWatch alarm namespace incorrect."; exit 1; }
echo "$CLOUDWATCH_ALARM" | jq -e '.change.after.threshold == 5' || { echo "Test Failed: CloudWatch alarm threshold incorrect."; exit 1; }
echo "$CLOUDWATCH_ALARM" | jq -e '.change.after.alarm_actions | type == "array" and length == 1' || { echo "Test Failed: CloudWatch alarm actions incorrect (expected 1 action). "; exit 1; }

echo "All tests passed!"

cd - > /dev/null
rm -rf "$TEMP_DIR"
