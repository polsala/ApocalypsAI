#!/bin/bash
set -euo pipefail

echo "--- Running Terraform tests for Digital Time Capsule ---"

# Change to the tests directory
cd "$(dirname "$0")"

# Initialize Terraform in the test directory
# -backend=false prevents Terraform from trying to configure a state backend,
# which is not needed for offline validation and plan generation.
echo "Initializing Terraform..."
terraform init -backend=false

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Generate an execution plan without applying it
echo "Generating Terraform plan..."
terraform plan -out=tfplan

# Show the plan in JSON format and perform assertions
echo "Inspecting Terraform plan..."
PLAN_JSON=$(terraform show -json tfplan)

# Mock rationale: This test uses `terraform plan -out=tfplan` and `terraform show -json tfplan` to generate and inspect the execution plan.
# This process is deterministic and offline as it does not interact with the actual AWS API.
# It verifies the module's output structure and resource configurations based on Terraform's internal logic,
# effectively "mocking" the cloud provider interaction by analyzing the *intended* actions rather than actual ones.

# Assertions on the plan
# Check if an aws_s3_bucket resource is planned for creation
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.actions[] == "create")' > /dev/null; then
  echo "ERROR: aws_s3_bucket resource not found in plan or not marked for creation."
  exit 1
fi

# Check if versioning is enabled
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket").change.after.versioning[0].enabled == true' > /dev/null; then
  echo "ERROR: S3 bucket versioning is not enabled in the plan."
  exit 1
fi

# Check for block public access settings
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket").change.after.block_public_acls == true' > /dev/null || \
   ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket").change.after.block_public_policy == true' > /dev/null || \
   ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket").change.after.ignore_public_acls == true' > /dev/null || \
   ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket").change.after.restrict_public_buckets == true' > /dev/null; then
  echo "ERROR: S3 bucket public access blocking is not fully configured in the plan."
  exit 1
fi

# Check for server-side encryption
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket").change.after.server_side_encryption_configuration[0].rule[0].apply_server_side_encryption_by_default[0].sse_algorithm == "AES256"' > /dev/null; then
  echo "ERROR: S3 bucket server-side encryption (AES256) is not configured in the plan."
  exit 1
fi

# Check for lifecycle rules (transition and expiration days)
# Note: jq path for lifecycle_rule can be tricky due to list of objects.
# We'll check for the presence of a lifecycle rule with specific properties.
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket").change.after.lifecycle_rule[] | select(.id == "glacier_transition_and_expiration" and .enabled == true and .transition[0].days == 30 and .expiration[0].days == 90)' > /dev/null; then
  echo "ERROR: S3 bucket lifecycle rule (glacier_transition_and_expiration) with expected days not found in the plan."
  exit 1
fi


echo "All Terraform plan assertions passed!"

# Clean up generated plan file
rm tfplan

echo "--- Terraform tests completed successfully! ---"
