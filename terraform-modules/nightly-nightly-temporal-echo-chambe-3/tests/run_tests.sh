#!/bin/bash
set -euo pipefail

echo "--- Running Terraform module tests ---"

# Change to the tests directory
cd "$(dirname "$0")"

# Initialize Terraform (backend=false for offline testing, no state file)
echo "Initializing Terraform..."
terraform init -backend=false -input=false

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Check Terraform formatting
echo "Checking Terraform formatting..."
terraform fmt -check

# Generate a plan and check for expected lifecycle rule
echo "Generating Terraform plan and checking for lifecycle rule..."
PLAN_OUTPUT=$(terraform plan -json -input=false -no-color)

# Check if the plan output contains the lifecycle rule for expiration_days
# Mock rationale: We are parsing the JSON plan output to assert the presence and value
# of the lifecycle rule, simulating a check against a real deployment without actual cloud interaction.
if echo "${PLAN_OUTPUT}" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_lifecycle_configuration" and .change.after.rule[0].expiration[0].days == 5)' > /dev/null; then
  echo "SUCCESS: Lifecycle rule with expiration_days = 5 found in plan."
else
  echo "ERROR: Lifecycle rule with expiration_days = 5 NOT found in plan."
  exit 1
fi

echo "All Terraform tests passed successfully!"
