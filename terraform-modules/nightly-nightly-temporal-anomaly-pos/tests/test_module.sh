#!/bin/bash
set -euo pipefail

MODULE_PATH="../src"

# Ensure jq is installed for JSON parsing
if ! command -v jq &> /dev/null
then
    echo "jq could not be found. Please install jq to run these tests." >&2
    exit 1
fi

echo "--- Initializing Terraform module ---"
terraform -chdir="$MODULE_PATH" init -backend=false # Mock rationale: -backend=false ensures no remote state operations, keeping the test offline.
echo "Terraform init successful."

echo "--- Validating Terraform syntax ---"
terraform -chdir="$MODULE_PATH" validate # Mock rationale: Validates HCL syntax and configuration without requiring cloud credentials.
echo "Terraform validation successful."

echo "--- Checking Terraform formatting ---"
terraform -chdir="$MODULE_PATH" fmt --check # Mock rationale: Ensures consistent code style, an offline check.
echo "Terraform formatting check successful."

echo "--- Generating Terraform plan for inspection ---"
terraform -chdir="$MODULE_PATH" plan -out=tfplan # Mock rationale: Generates an execution plan without applying, allowing inspection of intended changes.
terraform -chdir="$MODULE_PATH" show -json tfplan > tfplan.json # Mock rationale: Exports the plan to JSON for programmatic assertion, offline.
echo "Terraform plan generated and exported to tfplan.json."

echo "--- Asserting planned resources and properties ---"

# Check if aws_instance resource is planned
if ! jq -e '.resource_changes[] | select(.type == "aws_instance" and .change.actions[] == "create")' tfplan.json > /dev/null; then
    echo "ERROR: aws_instance resource not found in plan." >&2
    exit 1
fi
echo "Assertion: aws_instance resource found in plan."

# Check if aws_security_group resource is planned
if ! jq -e '.resource_changes[] | select(.type == "aws_security_group" and .change.actions[] == "create")' tfplan.json > /dev/null; then
    echo "ERROR: aws_security_group resource not found in plan." >&2
    exit 1
fi
echo "Assertion: aws_security_group resource found in plan."

# Check if aws_s3_bucket resource is planned
if ! jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.actions[] == "create")' tfplan.json > /dev/null; then
    echo "ERROR: aws_s3_bucket resource not found in plan." >&2
    exit 1
fi
echo "Assertion: aws_s3_bucket resource found in plan."

# Check for specific instance type (e.g., t2.micro default)
if ! jq -e '.resource_changes[] | select(.type == "aws_instance" and .change.after.instance_type == "t2.micro")' tfplan.json > /dev/null; then
    echo "ERROR: aws_instance with default 't2.micro' type not found in plan." >&2
    exit 1
fi
echo "Assertion: aws_instance with 't2.micro' type found in plan."

# Check for specific security group ingress rules (port 22 and 80)
if ! jq -e '.resource_changes[] | select(.type == "aws_security_group" and .change.after.ingress[] | select(.from_port == 22 and .to_port == 22 and .protocol == "tcp" and .cidr_blocks[] == "0.0.0.0/0"))' tfplan.json > /dev/null; then
    echo "ERROR: Security group ingress rule for SSH (port 22) not found." >&2
    exit 1
fi
echo "Assertion: Security group ingress rule for SSH (port 22) found."

if ! jq -e '.resource_changes[] | select(.type == "aws_security_group" and .change.after.ingress[] | select(.from_port == 80 and .to_port == 80 and .protocol == "tcp" and .cidr_blocks[] == "0.0.0.0/0"))' tfplan.json > /dev/null; then
    echo "ERROR: Security group ingress rule for HTTP (port 80) not found." >&2
    exit 1
fi
echo "Assertion: Security group ingress rule for HTTP (port 80) found."

echo "All assertions passed. Terraform module test successful!"

# Clean up generated plan files
rm "$MODULE_PATH/tfplan" "$MODULE_PATH/tfplan.json" # Mock rationale: Clean up temporary files generated during the offline test.
