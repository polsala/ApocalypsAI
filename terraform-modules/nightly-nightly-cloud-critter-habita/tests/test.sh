#!/bin/bash
set -e

# Mock rationale: This test runs `terraform plan` locally, which is an offline operation.
# It uses `terraform show -json` to inspect the generated plan, verifying that the module
# *would* create the expected resources with the correct properties, without actually
# interacting with the AWS API. The `ami_id` is hardcoded in `tests/main.tf` to ensure
# deterministic plan generation without relying on `data "aws_ami"` which fetches live data.

echo "Running Terraform module tests..."

# Change to the tests directory
cd "$(dirname "$0")"

# Initialize Terraform (no backend for local testing)
terraform init -backend=false

# Plan the infrastructure and save the plan to a file
terraform plan -out=tfplan

# Show the plan in JSON format
terraform show -json tfplan > tfplan.json

# --- Assertions ---

# Check if an aws_instance resource is planned
if ! jq -e '.resource_changes[] | select(.type == "aws_instance")' tfplan.json > /dev/null; then
  echo "Error: aws_instance not found in plan."
  exit 1
fi

# Check if an aws_security_group resource is planned
if ! jq -e '.resource_changes[] | select(.type == "aws_security_group")' tfplan.json > /dev/null; then
  echo "Error: aws_security_group not found in plan."
  exit 1
fi

# Check if an aws_cloudwatch_log_group resource is planned
if ! jq -e '.resource_changes[] | select(.type == "aws_cloudwatch_log_group")' tfplan.json > /dev/null; then
  echo "Error: aws_cloudwatch_log_group not found in plan."
  exit 1
fi

# Check instance type is 't2.nano' as specified in test config
if ! jq -e '.resource_changes[] | select(.type == "aws_instance" and .change.after.instance_type == "t2.nano")' tfplan.json > /dev/null; then
  echo "Error: aws_instance instance_type is not 't2.nano'."
  exit 1
fi

# Check critter_name is 'TestCritter' in the log group name
if ! jq -e '.resource_changes[] | select(.type == "aws_cloudwatch_log_group" and .change.after.name == "/aws/ec2/critter-habitat-TestCritter")' tfplan.json > /dev/null; then
  echo "Error: CloudWatch Log Group name does not contain 'TestCritter'."
  exit 1
fi

# Check key_name is 'test-key' as specified in test config
if ! jq -e '.resource_changes[] | select(.type == "aws_instance" and .change.after.key_name == "test-key")' tfplan.json > /dev/null; then
  echo "Error: aws_instance key_name is not 'test-key'."
  exit 1
fi

# Check for expected outputs
if ! jq -e '.planned_values.outputs.instance_public_ip' tfplan.json > /dev/null; then
  echo "Error: Output 'instance_public_ip' not found in plan."
  exit 1
fi

if ! jq -e '.planned_values.outputs.log_group_name' tfplan.json > /dev/null; then
  echo "Error: Output 'log_group_name' not found in plan."
  exit 1
fi

echo "All Terraform plan assertions passed!"

# Clean up generated plan files
rm tfplan tfplan.json
