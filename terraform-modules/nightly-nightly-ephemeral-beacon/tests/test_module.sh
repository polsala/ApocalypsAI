#!/bin/bash
set -euo pipefail

# Mock rationale: This test is deterministic and offline.
# It validates the Terraform module's syntax and structure using `terraform validate`
# and checks the output of `terraform plan` for expected resource creation,
# without requiring actual AWS credentials or deploying any resources.
# The AWS provider configuration is minimal and doesn't require authentication for `validate` or `plan`.

echo "--- Running Terraform module tests ---"

# Create a temporary directory for the test
TEST_DIR=$$(mktemp -d)
echo "Working in temporary directory: $TEST_DIR"
cd "$TEST_DIR"

# Create a minimal Terraform configuration to use the module
cat <<EOF > main.tf
provider "aws" {
  region = "us-east-1" # Mock region, no actual auth needed for plan/validate
}

resource "aws_security_group" "test_sg" {
  name        = "test-beacon-sg"
  description = "Allow all outbound traffic for testing"
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

module "ephemeral_beacon" {
  source = "../" # Path to the module under test

  region             = "us-east-1"
  instance_type      = "t3.nano"
  ami_id             = "ami-0abcdef1234567890" # Mock AMI ID
  key_name           = "my-ssh-key" # Mock key name
  beacon_count       = 1
  task_script        = "echo 'Hello from beacon!'"
  self_terminate     = false
  security_group_ids = [aws_security_group.test_sg.id]
  # log_bucket_name = "my-beacon-logs-bucket" # Optional, not needed for basic test
}
EOF

echo "Initializing Terraform..."
terraform init -backend=false > /dev/null # -backend=false for offline init
if [ $$? -ne 0 ]; then
    echo "ERROR: Terraform init failed."
    exit 1
fi
echo "Terraform init successful."

echo "Validating Terraform configuration..."
terraform validate
if [ $$? -ne 0 ]; then
    echo "ERROR: Terraform validation failed."
    exit 1
fi
echo "Terraform validation successful."

echo "Generating Terraform plan..."
PLAN_OUTPUT=$$(terraform plan -no-color)
if [ $$? -ne 0 ]; then
    echo "ERROR: Terraform plan generation failed."
    exit 1
fi
echo "Terraform plan generated."

# Assertions on the plan output
echo "Checking plan output for expected resources..."

# Expect 3 resources to add (aws_iam_role, aws_iam_role_policy, aws_iam_instance_profile, aws_launch_template, aws_ec2_instance, aws_security_group)
# The test config adds a security group, so total resources are 6.
if ! echo "$PLAN_OUTPUT" | grep -q "Plan: 6 to add, 0 to change, 0 to destroy."; then
    echo "ERROR: Expected '6 to add' in plan output, but got something else."
    echo "$PLAN_OUTPUT"
    exit 1
fi

# Expect an aws_instance resource to be created
if ! echo "$PLAN_OUTPUT" | grep -q "resource \"aws_ec2_instance\" \"beacon\""; then
    echo "ERROR: Expected 'aws_ec2_instance' resource in plan output."
    echo "$PLAN_OUTPUT"
    exit 1
fi

# Expect the instance type to be t3.nano
if ! echo "$PLAN_OUTPUT" | grep -q 'instance_type = "t3.nano"'; then
    echo "ERROR: Expected instance_type 't3.nano' in plan output."
    echo "$PLAN_OUTPUT"
    exit 1
fi

# Expect the IAM role to be created
if ! echo "$PLAN_OUTPUT" | grep -q "resource \"aws_iam_role\" \"beacon_role\""; then
    echo "ERROR: Expected 'aws_iam_role' resource in plan output."
    echo "$PLAN_OUTPUT"
    exit 1
fi

echo "All Terraform module tests passed successfully!"

# Clean up temporary directory
cd - > /dev/null
rm -rf "$TEST_DIR"
echo "Cleaned up temporary directory: $TEST_DIR"
