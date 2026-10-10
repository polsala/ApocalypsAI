#!/bin/bash
set -euo pipefail

# Mock rationale: This test script operates entirely offline by analyzing the output
# of `terraform plan -json`. It does not interact with any actual cloud provider APIs.
# The `terraform plan` command itself is deterministic given a set of input files
# and variables, producing a JSON representation of the intended infrastructure changes.
# `jq` is used to parse this local, static JSON output, ensuring the test is
# self-contained and does not require external network access or cloud credentials
# beyond what Terraform itself needs to *parse* the configuration (which is minimal
# for a plan, not an apply).

echo "Starting Nightly Temporal Sandbox Terraform plan tests..."

# Create a temporary directory for Terraform operations
TEST_DIR=$(mktemp -d)
echo "Using temporary directory: $TEST_DIR"
cp -r ../src/* "$TEST_DIR/"
cd "$TEST_DIR"

# Initialize Terraform
echo "Initializing Terraform..."
terraform init -backend=false > /dev/null # -backend=false for offline testing
if [ $? -ne 0 ]; then
    echo "Terraform init failed!"
    exit 1
fi
echo "Terraform init successful."

# Run terraform plan and capture JSON output
echo "Generating Terraform plan JSON..."
PLAN_OUTPUT=$(terraform plan -out=tfplan.binary -json -var="sandbox_name=test-sandbox" -var="ttl_hours=1" 2>&1)
if [ $? -ne 0 ]; then
    echo "Terraform plan failed!"
    echo "$PLAN_OUTPUT"
    exit 1
fi
echo "Terraform plan generated."

# Extract the JSON part from the plan output (it might contain other logs)
# The actual plan JSON is usually prefixed with a specific marker or is the last JSON object.
# For simplicity, we'll assume the `terraform plan -json` output is mostly JSON.
# A more robust approach would be to parse the entire output and find the object of type "plan".
# For this test, we'll just try to parse the whole thing.
PLAN_JSON=$(terraform show -json tfplan.binary)

# Test 1: Verify that an aws_vpc resource is planned
echo "Test 1: Verifying aws_vpc resource..."
if echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_vpc" and .change.actions[] == "create")' > /dev/null; then
    echo "  PASS: aws_vpc resource found in plan."
else
    echo "  FAIL: aws_vpc resource not found in plan."
    exit 1
fi

# Test 2: Verify that an aws_instance resource is planned
echo "Test 2: Verifying aws_instance resource..."
if echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_instance" and .change.actions[] == "create")' > /dev/null; then
    echo "  PASS: aws_instance resource found in plan."
else
    echo "  FAIL: aws_instance resource not found in plan."
    exit 1
fi

# Test 3: Verify that the aws_instance has an ExpiryDate tag
echo "Test 3: Verifying aws_instance has ExpiryDate tag..."
if echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_instance" and .change.actions[] == "create") | .change.after.tags.ExpiryDate' > /dev/null; then
    echo "  PASS: aws_instance has ExpiryDate tag."
else
    echo "  FAIL: aws_instance does not have ExpiryDate tag."
    exit 1
fi

# Test 4: Verify that the expiry_timestamp output is present and is a valid RFC3339 format
echo "Test 4: Verifying expiry_timestamp output..."
EXPIRY_OUTPUT=$(echo "$PLAN_JSON" | jq -r '.planned_values.outputs.expiry_timestamp.value')
if [[ "$EXPIRY_OUTPUT" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$ ]]; then
    echo "  PASS: expiry_timestamp output is present and in RFC3339 format: $EXPIRY_OUTPUT"
else
    echo "  FAIL: expiry_timestamp output is missing or not in RFC3339 format: $EXPIRY_OUTPUT"
    exit 1
fi

echo "All tests passed for Nightly Temporal Sandbox."

# Clean up temporary directory
cd - > /dev/null
rm -rf "$TEST_DIR"
echo "Cleaned up temporary directory: $TEST_DIR"
