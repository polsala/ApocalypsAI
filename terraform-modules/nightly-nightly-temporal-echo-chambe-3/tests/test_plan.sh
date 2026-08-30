#!/bin/bash

set -euo pipefail

# Mock rationale: This test performs a 'terraform plan' which is a dry-run operation.
# It does not interact with actual AWS APIs. The assertions are based on the structure
# and content of the generated plan file, which is deterministic given the module's
# source code and mock input variables. No external services are called during this test.

# Create a temporary directory for the test
TEST_DIR=$(mktemp -d)
cleanup() {
  rm -rf "$TEST_DIR"
}
trap cleanup EXIT

# Copy module source to the test directory
cp -R ../src/* "$TEST_DIR/"

# Create a mock root module configuration for testing
cat <<EOF > "$TEST_DIR/test_root.tf"
module "temporal_echo_chamber" {
  source = "."

  region        = "us-east-1"
  instance_type = "t2.micro"
  ami_id        = "ami-0abcdef1234567890" # Mock AMI ID
  key_name      = "mock-key"
  vpc_cidr      = "10.0.0.0/16"
  subnet_cidr   = "10.0.1.0/24"
  allowed_ssh_cidr = "192.168.1.1/32"

  tags = {
    Project     = "TestProject"
    Environment = "TestEchoChamber"
  }
}
EOF

cd "$TEST_DIR"

echo "Initializing Terraform..."
terraform init -backend=false > /dev/null

echo "Running Terraform plan..."
PLAN_OUTPUT=$(terraform plan -out=tfplan -no-color)

# Check if plan was successful and shows 7 resources to add
if ! echo "$PLAN_OUTPUT" | grep -q "Plan: 7 to add, 0 to change, 0 to destroy."; then
  echo "Test Failed: Expected '7 to add' in plan summary."
  echo "--- Terraform Plan Output ---"
  echo "$PLAN_OUTPUT"
  exit 1
fi

# Verify specific resources are planned for creation using terraform show -json
echo "Verifying planned resources..."
JSON_PLAN=$(terraform show -json tfplan)

# Check for aws_vpc
if ! echo "$JSON_PLAN" | grep -q '"type": "aws_vpc"'; then
  echo "Test Failed: aws_vpc resource not found in plan."
  exit 1
fi

# Check for aws_instance
if ! echo "$JSON_PLAN" | grep -q '"type": "aws_instance"'; then
  echo "Test Failed: aws_instance resource not found in plan."
  exit 1
fi

# Check for aws_subnet
if ! echo "$JSON_PLAN" | grep -q '"type": "aws_subnet"'; then
  echo "Test Failed: aws_subnet resource not found in plan."
  exit 1
fi

# Check for aws_security_group
if ! echo "$JSON_PLAN" | grep -q '"type": "aws_security_group"'; then
  echo "Test Failed: aws_security_group resource not found in plan."
  exit 1
fi

# Check for aws_internet_gateway
if ! echo "$JSON_PLAN" | grep -q '"type": "aws_internet_gateway"'; then
  echo "Test Failed: aws_internet_gateway resource not found in plan."
  exit 1
fi

# Check for aws_route_table
if ! echo "$JSON_PLAN" | grep -q '"type": "aws_route_table"'; then
  echo "Test Failed: aws_route_table resource not found in plan."
  exit 1
fi

# Check for aws_route_table_association
if ! echo "$JSON_PLAN" | grep -q '"type": "aws_route_table_association"'; then
  echo "Test Failed: aws_route_table_association resource not found in plan."
  exit 1
fi

# Check for specific instance type in the plan
if ! echo "$JSON_PLAN" | grep -q '"instance_type": {
            "new": "t2.micro"'; then
  echo "Test Failed: Expected instance_type 't2.micro' not found in plan."
  exit 1
fi

# Check for specific VPC CIDR in the plan
if ! echo "$JSON_PLAN" | grep -q '"cidr_block": {
            "new": "10.0.0.0/16"'; then
  echo "Test Failed: Expected vpc_cidr '10.0.0.0/16' not found in plan."
  exit 1
fi

# Check for specific SSH CIDR in the plan
if ! echo "$JSON_PLAN" | grep -q '"cidr_blocks": [
              "192.168.1.1/32"
            ]'; then
  echo "Test Failed: Expected allowed_ssh_cidr '192.168.1.1/32' not found in plan."
  exit 1
fi


echo "All Terraform plan checks passed successfully!"
