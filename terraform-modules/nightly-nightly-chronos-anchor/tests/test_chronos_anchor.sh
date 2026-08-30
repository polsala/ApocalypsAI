#!/bin/bash
set -euo pipefail

# Mock rationale: This test script uses `terraform validate` and `terraform plan`
# which are offline operations when run against a local module.
# It does not interact with actual cloud providers.
# The `mock_tf_config` directory provides a minimal configuration to instantiate
# the module, allowing for syntax and basic plan output checks.

echo "--- Running Chronos Anchor Terraform Module Tests ---"

TEST_DIR="mock_tf_config"
MODULE_PATH="../src"

# Ensure Terraform is installed
if ! command -v terraform &> /dev/null
then
    echo "Error: Terraform is not installed. Please install it to run these tests."
    exit 1
fi

# Clean up previous runs
rm -rf "$TEST_DIR/.terraform" "$TEST_DIR/.terraform.lock.hcl" "$TEST_DIR/terraform.tfstate*" "$TEST_DIR/tfplan"

echo "1. Initializing Terraform in $TEST_DIR..."
if ! terraform -chdir="$TEST_DIR" init -backend=false -upgrade &> /dev/null; then
    echo "FAIL: Terraform init failed."
    exit 1
fi
echo "PASS: Terraform init successful."

echo "2. Validating Terraform configuration..."
if ! terraform -chdir="$TEST_DIR" validate &> /dev/null; then
    echo "FAIL: Terraform validation failed."
    exit 1
fi
echo "PASS: Terraform configuration is valid."

echo "3. Generating Terraform plan and checking for expected tags..."
PLAN_OUTPUT=$(terraform -chdir="$TEST_DIR" plan -no-color -out=tfplan)
if echo "$PLAN_OUTPUT" | grep -q 'resource "aws_s3_bucket" "chronos_anchor_bucket"'; then
    echo "  - Found expected S3 bucket resource."
else
    echo "FAIL: S3 bucket resource not found in plan output."
    echo "$PLAN_OUTPUT"
    exit 1
fi

if echo "$PLAN_OUTPUT" | grep -q 'chronos_epoch = "[^\"]\+"'; then
    echo "  - Found 'chronos_epoch' tag in plan output."
else
    echo "FAIL: 'chronos_epoch' tag not found in plan output."
    echo "$PLAN_OUTPUT"
    exit 1
fi

if echo "$PLAN_OUTPUT" | grep -q 'chronos_decay_days = 42'; then
    echo "  - Found 'chronos_decay_days = 42' tag in plan output (from mock config)."
else
    echo "FAIL: 'chronos_decay_days = 42' tag not found in plan output."
    echo "$PLAN_OUTPUT"
    exit 1
fi

if echo "$PLAN_OUTPUT" | grep -q 'ManagedBy = "ApocalypsAI-ChronosAnchor"'; then
    echo "  - Found 'ManagedBy' tag in plan output."
else
    echo "FAIL: 'ManagedBy' tag not found in plan output."
    echo "$PLAN_OUTPUT"
    exit 1
fi

echo "PASS: Terraform plan generated and expected tags found."

echo "4. Ensuring plan can be destroyed (no errors on destroy plan)..."
if ! terraform -chdir="$TEST_DIR" plan -destroy -no-color &> /dev/null; then
    echo "FAIL: Terraform destroy plan failed."
    exit 1
fi
echo "PASS: Terraform destroy plan successful."

echo "--- All Chronos Anchor Terraform Module Tests Passed! ---"

# Clean up generated plan file
rm -f "$TEST_DIR/tfplan"
