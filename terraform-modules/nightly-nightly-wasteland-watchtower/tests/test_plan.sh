#!/bin/bash
set -euo pipefail

# Mock rationale: This test performs an offline validation and plan inspection
# using Terraform's built-in capabilities. It does not interact with actual
# AWS resources, making it deterministic and offline. It uses a temporary
# directory and dummy variable values to simulate a deployment plan.

echo "--- Running Terraform tests for Nightly Wasteland Watchtower ---"

# Check for required tools
if ! command -v terraform &> /dev/null; then
    echo "ERROR: terraform command not found. Please install Terraform."
    exit 1
fi
if ! command -v jq &> /dev/null; then
    echo "ERROR: jq command not found. Please install jq."
    exit 1
fi

# Create a temporary directory for the test
TEST_DIR=$(mktemp -d)
cp -R src/* "$TEST_DIR/"
cd "$TEST_DIR"

# Override variables for testing
cat <<EOF > test_override.tfvars
region        = "us-east-1"
ami_id        = "ami-0abcdef1234567890" # A dummy AMI ID for plan validation
instance_type = "t2.micro"
key_name      = "test-key-pair"
EOF

echo "1. Running terraform init..."
# -backend=false ensures no remote state configuration is attempted
terraform init -backend=false > /dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: terraform init failed."
    cd - > /dev/null
    rm -rf "$TEST_DIR"
    exit 1
fi
echo "   terraform init successful."

echo "2. Running terraform validate..."
terraform validate
if [ $? -ne 0 ]; then
    echo "ERROR: terraform validate failed."
    cd - > /dev/null
    rm -rf "$TEST_DIR"
    exit 1
fi
echo "   terraform validate successful."

echo "3. Generating terraform plan and inspecting output..."
# -out=tfplan saves the plan to a file for inspection
terraform plan -var-file=test_override.tfvars -out=tfplan > /dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: terraform plan failed."
    cd - > /dev/null
    rm -rf "$TEST_DIR"
    exit 1
fi

# Inspect the plan JSON
PLAN_JSON=$(terraform show -json tfplan)

# Test 3.1: Check if aws_instance resource is planned for creation
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_instance" and .change.actions[] == "create")' > /dev/null; then
    echo "ERROR: aws_instance resource not found in plan or not marked for creation."
    cd - > /dev/null
    rm -rf "$TEST_DIR"
    exit 1
fi
echo "   aws_instance resource found and marked for creation."

# Test 3.2: Check if aws_security_group resource is planned for creation
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_security_group" and .change.actions[] == "create")' > /dev/null; then
    echo "ERROR: aws_security_group resource not found in plan or not marked for creation."
    cd - > /dev/null
    rm -rf "$TEST_DIR"
    exit 1
fi
echo "   aws_security_group resource found and marked for creation."

# Test 3.3: Check instance_type in the planned instance
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_instance" and .change.after.instance_type == "t2.micro")' > /dev/null; then
    echo "ERROR: aws_instance does not have expected instance_type 't2.micro'."
    cd - > /dev/null
    rm -rf "$TEST_DIR"
    exit 1
fi
echo "   aws_instance has expected instance_type 't2.micro'."

# Test 3.4: Check AMI ID in the planned instance
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_instance" and .change.after.ami == "ami-0abcdef1234567890")' > /dev/null; then
    echo "ERROR: aws_instance does not have expected ami_id 'ami-0abcdef1234567890'."
    cd - > /dev/null
    rm -rf "$TEST_DIR"
    exit 1
fi
echo "   aws_instance has expected ami_id 'ami-0abcdef1234567890'."

# Test 3.5: Check if SSH ingress rule (port 22) is present in the security group
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_security_group" and .change.after.ingress[] | select(.from_port == 22 and .to_port == 22 and .protocol == "tcp" and .cidr_blocks[] | contains("0.0.0.0/0")))' > /dev/null; then
    echo "ERROR: Security group does not have expected SSH ingress rule (port 22)."
    cd - > /dev/null
    rm -rf "$TEST_DIR"
    exit 1
fi
echo "   Security group has expected SSH ingress rule (port 22)."

# Test 3.6: Check if HTTP ingress rule (port 80) is present in the security group
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_security_group" and .change.after.ingress[] | select(.from_port == 80 and .to_port == 80 and .protocol == "tcp" and .cidr_blocks[] | contains("0.0.0.0/0")))' > /dev/null; then
    echo "ERROR: Security group does not have expected HTTP ingress rule (port 80)."
    cd - > /dev/null
    rm -rf "$TEST_DIR"
    exit 1
fi
echo "   Security group has expected HTTP ingress rule (port 80)."

echo "--- All Terraform tests passed! ---"

# Clean up
cd - > /dev/null
rm -rf "$TEST_DIR"
