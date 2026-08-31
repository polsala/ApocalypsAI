#!/bin/bash

set -euo pipefail

TEST_DIR="$(dirname "$0")"
MODULE_DIR="${TEST_DIR}/../src"

echo "--- Running Terraform module tests ---"

# Clean up previous Terraform state
rm -rf "${TEST_DIR}/.terraform" "${TEST_DIR}/.terraform.lock.hcl" "${TEST_DIR}/terraform.tfstate*"

echo "Initializing Terraform in ${TEST_DIR}..."
# Mock rationale: 'terraform init' downloads necessary providers.
# While it hits the internet, it's a prerequisite for 'terraform plan' and
# does not interact with actual cloud resources for this test setup.
# The providers are then cached locally.
terraform -chdir="${TEST_DIR}" init -backend=false -upgrade

echo "Validating Terraform configuration..."
# Mock rationale: 'terraform validate' performs syntax and basic semantic checks
# without needing to interact with cloud APIs. It's fully offline after init.
terraform -chdir="${TEST_DIR}" validate

echo "Generating Terraform plan and checking output..."
# Mock rationale: 'terraform plan' with mock providers generates a plan
# based on the provided configuration and mocked data sources. It does not
# interact with actual cloud resources. We check the *content* of this plan
# to ensure the module logic is correct.
PLAN_OUTPUT=$(terraform -chdir="${TEST_DIR}" plan -no-color -var "source_instance_id=i-mocksourceinstanceid" -var "target_region=us-west-1" -var "replica_name_prefix=test-echo" -var "ami_override=ami-mockoverrideami" -var "instance_type_override=t3.small" -var "tags_to_add={TestTag=TestValue}" -var "subnet_id=subnet-mockdefaultsubnetid" -var "security_group_ids=[\"sg-mockdefaultsgid\"]" 2>&1)

echo "${PLAN_OUTPUT}"

# Assertions based on the plan output
# Check if an aws_instance resource named 'echo' is planned for creation
if ! echo "${PLAN_OUTPUT}" | grep -q 'resource "aws_instance" "echo" {'; then
  echo "Test Failed: Expected 'aws_instance.echo' resource not found in plan."
  exit 1
fi

# Check if the AMI override is applied
if ! echo "${PLAN_OUTPUT}" | grep -q 'ami = "ami-mockoverrideami"'; then
  echo "Test Failed: AMI override not applied correctly."
  exit 1
fi

# Check if the instance type override is applied
if ! echo "${PLAN_OUTPUT}" | grep -q 'instance_type = "t3.small"'; then
  echo "Test Failed: Instance type override not applied correctly."
  exit 1
fi

# Check if the replica name prefix is applied in tags
if ! echo "${PLAN_OUTPUT}" | grep -q 'Name = "test-echo-i-mocksourceinstanceid"'; then
  echo "Test Failed: Replica name prefix not applied correctly in Name tag."
  exit 1
fi

# Check if custom tags are added
if ! echo "${PLAN_OUTPUT}" | grep -q 'TestTag = "TestValue"'; then
  echo "Test Failed: Custom tags not added correctly."
  exit 1
fi

# Check if source instance ID tag is present
if ! echo "${PLAN_OUTPUT}" | grep -q 'TemporalEchoSourceInstance = "i-mocksourceinstanceid"'; then
  echo "Test Failed: Source instance ID tag not found."
  exit 1
fi

# Check if source region tag is present
if ! echo "${PLAN_OUTPUT}" | grep -q 'TemporalEchoSourceRegion = "us-east-1a"'; then
  echo "Test Failed: Source region tag not found."
  exit 1
fi

# Check if target region tag is present
if ! echo "${PLAN_OUTPUT}" | grep -q 'TemporalEchoTargetRegion = "us-west-1"'; then
  echo "Test Failed: Target region tag not found."
  exit 1

fi

# Check if subnet_id is set
if ! echo "${PLAN_OUTPUT}" | grep -q 'subnet_id = "subnet-mockdefaultsubnetid"'; then
  echo "Test Failed: Subnet ID not set correctly."
  exit 1
fi

# Check if security_group_ids is set
if ! echo "${PLAN_OUTPUT}" | grep -q 'vpc_security_group_ids = \[ "sg-mockdefaultsgid", \]'; then
  echo "Test Failed: Security Group IDs not set correctly."
  exit 1
fi

echo "All Terraform plan assertions passed!"
echo "--- Tests completed successfully ---"
