#!/bin/bash

set -euo pipefail

TEST_DIR="$(mktemp -d)"
MODULE_PATH="$(dirname "$0")"/../src

cleanup() {
  echo "Cleaning up test directory: $TEST_DIR"
  rm -rf "$TEST_DIR"
}

trap cleanup EXIT

echo "Running Terraform module tests in $TEST_DIR"

# Create a temporary root module to test the ephemeral-cloud-nest module
cat <<EOF > "$TEST_DIR/main.tf"
provider "aws" {
  region = "us-east-1"
  # Mock rationale: For offline testing, we don't need actual AWS credentials.
  # Terraform init will download the provider, but plan will not interact with AWS.
  # We use dummy credentials to satisfy the provider block syntax.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "ephemeral_nest" {
  source = "$MODULE_PATH"

  project_name = "test-nest"
  instance_type = "t2.micro"
  ami_id = "ami-0abcdef1234567890" # A dummy AMI ID for testing
  ttl_hours = 2
  key_name = "test-key"
  availability_zone = "us-east-1a"
}
EOF

# Test 1: Terraform Init and Validate
echo "\n--- Test 1: Terraform Init and Validate ---"
(cd "$TEST_DIR" && terraform init -backend=false -input=false)
if [ $? -ne 0 ]; then
  echo "FAIL: Terraform init failed."
  exit 1
fi

(cd "$TEST_DIR" && terraform validate)
if [ $? -ne 0 ]; then
  echo "FAIL: Terraform validate failed."
  exit 1
fi
echo "PASS: Terraform init and validate successful."

# Test 2: Terraform Plan - Check for expected resources and tags
echo "\n--- Test 2: Terraform Plan - Check resources and tags ---"
# Mock rationale: We are parsing the JSON output of 'terraform plan'.
# This output describes the intended changes without making any actual API calls.
# By asserting on the structure and content of this plan, we deterministically
# verify the module's behavior offline. 'jq' is used to parse the JSON.
PLAN_OUTPUT=$(cd "$TEST_DIR" && terraform plan -json -input=false -var 'ami_id=ami-0abcdef1234567890')

# Check for VPC
if ! echo "$PLAN_OUTPUT" | jq -e '.resource_changes[] | select(.type == "aws_vpc" and .change.actions[] == "create")' > /dev/null; then
  echo "FAIL: aws_vpc resource not found in plan."
  exit 1
fi

# Check for Subnet
if ! echo "$PLAN_OUTPUT" | jq -e '.resource_changes[] | select(.type == "aws_subnet" and .change.actions[] == "create")' > /dev/null; then
  echo "FAIL: aws_subnet resource not found in plan."
  exit 1
fi

# Check for Security Group
if ! echo "$PLAN_OUTPUT" | jq -e '.resource_changes[] | select(.type == "aws_security_group" and .change.actions[] == "create")' > /dev/null; then
  echo "FAIL: aws_security_group resource not found in plan."
  exit 1
fi

# Check for EC2 Instance
if ! echo "$PLAN_OUTPUT" | jq -e '.resource_changes[] | select(.type == "aws_instance" and .change.actions[] == "create")' > /dev/null; then
  echo "FAIL: aws_instance resource not found in plan."
  exit 1
fi

# Check for specific tags on VPC (e.g., ephemeral and ttl)
if ! echo "$PLAN_OUTPUT" | jq -e '.resource_changes[] | select(.type == "aws_vpc" and .change.after.tags.ephemeral == "true" and .change.after.tags.ttl == "2h")' > /dev/null; then
  echo "FAIL: aws_vpc missing ephemeral or ttl tags, or incorrect values."
  exit 1
fi

# Check for instance type on EC2 instance
if ! echo "$PLAN_OUTPUT" | jq -e '.resource_changes[] | select(.type == "aws_instance" and .change.after.instance_type == "t2.micro")' > /dev/null; then
  echo "FAIL: aws_instance has incorrect instance_type."
  exit 1
fi

echo "PASS: Terraform plan includes expected resources and tags."

# Test 3: Check outputs
echo "\n--- Test 3: Check outputs ---"
# Mock rationale: We are checking the outputs defined in the module.
# 'terraform plan -json' includes the planned outputs, which can be verified offline.
# We ensure that the module declares the expected outputs.

# Check for vpc_id output
if ! echo "$PLAN_OUTPUT" | jq -e '.planned_values.outputs.vpc_id' > /dev/null; then
  echo "FAIL: vpc_id output not found in plan."
  exit 1
fi

# Check for instance_public_ip output
if ! echo "$PLAN_OUTPUT" | jq -e '.planned_values.outputs.instance_public_ip' > /dev/null; then
  echo "FAIL: instance_public_ip output not found in plan."
  exit 1
fi

echo "PASS: Terraform plan includes expected outputs."

echo "\nAll tests passed successfully!"
