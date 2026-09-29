#!/bin/bash
set -euo pipefail

echo "--- Running Terraform module tests for Nightly Cloud Critter Catcher ---"

# Change to the tests directory
cd "$(dirname "$0")"

# Clean up previous runs
rm -rf .terraform .terraform.lock.hcl terraform.tfstate* tfplan*

# Mock rationale: `terraform init -backend=false` initializes the working directory
# without configuring a backend, preventing network calls for state management.
# This allows for offline syntax and plan validation.
echo "1. Initializing Terraform..."
terraform init -backend=false > /dev/null

# Mock rationale: `terraform validate` checks the configuration syntax and internal
# consistency without making any API calls to AWS.
echo "2. Validating Terraform configuration..."
terraform validate

# Mock rationale: `terraform plan -no-color -input=false` generates an execution plan
# without prompting for input and without applying changes. The `-no-color` flag
# ensures consistent output for grep. This is an offline operation.
echo "3. Generating Terraform plan and asserting outputs..."
PLAN_OUTPUT=$(terraform plan -no-color -input=false)

# Assertions using grep
echo "$PLAN_OUTPUT" | grep -q 'resource "aws_instance" "critter"' || { echo "Test failed: aws_instance resource not found in plan."; exit 1; }
echo "$PLAN_OUTPUT" | grep -q 'Name: "Critter-test-critter-alpha"' || { echo "Test failed: Critter-test-critter-alpha tag not found."; exit 1; }
echo "$PLAN_OUTPUT" | grep -q 'instance_type: "t2.micro"' || { echo "Test failed: t2.micro instance type not found."; exit 1; }
echo "$PLAN_OUTPUT" | grep -q 'lifespan is 5 minutes' || { echo "Test failed: Lifespan 5 minutes not found in user_data."; exit 1; }
echo "$PLAN_OUTPUT" | grep -q 'shutdown -h +5' || { echo "Test failed: Shutdown command for 5 minutes not found in user_data."; exit 1; }

echo "$PLAN_OUTPUT" | grep -q 'Name: "Critter-test-critter-beta"' || { echo "Test failed: Critter-test-critter-beta tag not found."; exit 1; }
echo "$PLAN_OUTPUT" | grep -q 'instance_type: "t3.small"' || { echo "Test failed: t3.small instance type not found."; exit 1; }
echo "$PLAN_OUTPUT" | grep -q 'lifespan is 15 minutes' || { echo "Test failed: Lifespan 15 minutes not found in user_data."; exit 1; }
echo "$PLAN_OUTPUT" | grep -q 'shutdown -h +15' || { echo "Test failed: Shutdown command for 15 minutes not found in user_data."; exit 1; }
echo "$PLAN_OUTPUT" | grep -q 'vpc_security_group_ids: \["sg-mock1", "sg-mock2"\]' || { echo "Test failed: Mock security group IDs not found."; exit 1; }
echo "$PLAN_OUTPUT" | grep -q 'subnet_id: "subnet-mock1"' || { echo "Test failed: Mock subnet ID not found."; exit 1; }


echo "All Terraform plan assertions passed!"

echo "--- Nightly Cloud Critter Catcher tests completed successfully! ---"

# Clean up generated files
rm -rf .terraform .terraform.lock.hcl terraform.tfstate* tfplan*
