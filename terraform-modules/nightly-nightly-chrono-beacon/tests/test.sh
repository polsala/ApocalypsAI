#!/bin/bash
set -euo pipefail

# Mock rationale: This test runs 'terraform plan' which is an offline operation.
# It validates the HCL syntax and resource graph without making actual cloud API calls.
# We assert on the *output* of the plan, which is deterministic given the input HCL.

echo "Running Terraform module tests..."

TEST_DIR=$(mktemp -d)
cp tests/main.tf "$TEST_DIR/"
cp -r src "$TEST_DIR/" # Copy the module source into the test directory

cd "$TEST_DIR"

echo "Initializing Terraform..."
terraform init -backend=false > /dev/null # -backend=false for offline testing
if [ $? -ne 0 ]; then
    echo "Terraform init failed!"
    exit 1
fi

echo "Running terraform plan..."
PLAN_OUTPUT=$(terraform plan -no-color -out=tfplan)
if [ $? -ne 0 ]; then
    echo "Terraform plan failed!"
    echo "$PLAN_OUTPUT"
    exit 1
fi

echo "Verifying planned resources..."

# Check for key resources in the plan output
if ! echo "$PLAN_OUTPUT" | grep -q "aws_lb.chrono_beacon_lb"; then
    echo "Error: aws_lb.chrono_beacon_lb not found in plan."
    exit 1
fi

if ! echo "$PLAN_OUTPUT" | grep -q "aws_lb_target_group.chrono_beacon_tg"; then
    echo "Error: aws_lb_target_group.chrono_beacon_tg not found in plan."
    exit 1
fi

if ! echo "$PLAN_OUTPUT" | grep -q "aws_launch_template.chrono_beacon_lt"; then
    echo "Error: aws_launch_template.chrono_beacon_lt not found in plan."
    exit 1
fi

if ! echo "$PLAN_OUTPUT" | grep -q "aws_autoscaling_group.chrono_beacon_asg"; then
    echo "Error: aws_autoscaling_group.chrono_beacon_asg not found in plan."
    exit 1
fi

if ! echo "$PLAN_OUTPUT" | grep -q "aws_security_group.chrono_beacon_lb_sg"; then
    echo "Error: aws_security_group.chrono_beacon_lb_sg not found in plan."
    exit 1
fi

if ! echo "$PLAN_OUTPUT" | grep -q "aws_security_group.chrono_beacon_instance_sg"; then
    echo "Error: aws_security_group.chrono_beacon_instance_sg not found in plan."
    exit 1
fi

# Check for specific attributes in the plan (e.g., instance type)
if ! echo "$PLAN_OUTPUT" | grep -q "instance_type = \"t2.micro\""; then
    echo "Error: Expected instance_type 't2.micro' not found in plan."
    exit 1
fi

echo "Terraform plan verification successful!"

# Clean up
cd - > /dev/null
rm -rf "$TEST_DIR"

echo "All tests passed for Nightly Chrono-Beacon!"
