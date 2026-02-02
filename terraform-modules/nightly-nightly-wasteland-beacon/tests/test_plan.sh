#!/bin/bash

set -euo pipefail

# Mock rationale: Terraform's 'plan' command, when run with specific variable inputs,
# generates a deterministic execution plan without making any API calls to the cloud provider.
# This allows us to verify the intended infrastructure configuration (resource types, properties, counts)
# offline. We use 'jq' to parse the JSON output of 'terraform show -json tfplan' and assert on the
# structure and content of the planned changes, effectively mocking the cloud provider's response to a 'plan' request.

echo "Running offline Terraform plan tests..."

# Create a temporary directory for the test run
mkdir -p .terraform-test
cp ../*.tf .terraform-test/
cd .terraform-test

# Initialize Terraform in the temporary directory
# We use -backend=false to avoid needing a real S3 backend for state in tests
terraform init -backend=false > /dev/null

# Validate the Terraform configuration syntax
echo "  - Validating Terraform syntax..."
terraform validate

# Generate a plan without applying, using mock variables
echo "  - Generating Terraform plan..."
terraform plan -out=tfplan \
  -var="region=us-east-1" \
  -var="instance_type=t2.micro" \
  -var="ami_id=ami-0abcdef1234567890" \
  -var="key_name=test-key" \
  -var="beacon_port=8080" \
  -var='tags={"Project":"ApocalypsAI", "Environment":"Test", "BeaconName":"AlphaBeacon"}' > /dev/null

# Show the plan in JSON format for assertions
terraform show -json tfplan > tfplan.json

# --- Assertions ---

# Check if EC2 instance is planned for creation
echo "  - Asserting aws_instance creation..."
if ! jq -e '.resource_changes[] | select(.type == "aws_instance" and .change.actions[] == "create")' tfplan.json > /dev/null; then
  echo "Error: aws_instance resource not found in plan or not marked for creation!"
  exit 1
fi

# Check if S3 bucket is planned for creation
echo "  - Asserting aws_s3_bucket creation..."
if ! jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.actions[] == "create")' tfplan.json > /dev/null; then
  echo "Error: aws_s3_bucket resource not found in plan or not marked for creation!"
  exit 1
fi

# Check if Security Group is planned for creation
echo "  - Asserting aws_security_group creation..."
if ! jq -e '.resource_changes[] | select(.type == "aws_security_group" and .change.actions[] == "create")' tfplan.json > /dev/null; then
  echo "Error: aws_security_group resource not found in plan or not marked for creation!"
  exit 1
fi

# Check if VPC is planned for creation
echo "  - Asserting aws_vpc creation..."
if ! jq -e '.resource_changes[] | select(.type == "aws_vpc" and .change.actions[] == "create")' tfplan.json > /dev/null; then
  echo "Error: aws_vpc resource not found in plan or not marked for creation!"
  exit 1
fi

# Check if the EC2 instance type is correctly set in the plan
echo "  - Asserting EC2 instance type..."
if ! jq -e '.resource_changes[] | select(.type == "aws_instance" and .change.after.instance_type == "t2.micro")' tfplan.json > /dev/null; then
  echo "Error: EC2 instance type is not 't2.micro' in the plan!"
  exit 1
fi

# Check if the beacon_port (8080) is correctly opened in the security group ingress rules
echo "  - Asserting beacon_port in Security Group..."
if ! jq -e '.resource_changes[] | select(.type == "aws_security_group" and .change.after.ingress[] | select(.from_port == 8080 and .to_port == 8080 and .protocol == "tcp"))' tfplan.json > /dev/null; then
  echo "Error: Beacon port 8080 not found in security group ingress rules!"
  exit 1
fi

# Check if the S3 bucket name follows the expected pattern (case-insensitive check for simplicity)
echo "  - Asserting S3 bucket name pattern..."
if ! jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.after.bucket | test("apocalypsai-alphabeacon-wasteland-beacon-storage"))' tfplan.json > /dev/null; then
  echo "Error: S3 bucket name does not match expected pattern!"
  exit 1
fi

echo "All offline Terraform plan tests passed!"

# Clean up generated files
cd ..
rm -rf .terraform-test
