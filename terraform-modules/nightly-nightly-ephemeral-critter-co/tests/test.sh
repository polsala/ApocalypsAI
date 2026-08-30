#!/bin/bash
set -euo pipefail

echo "Running offline Terraform module tests for nightly-ephemeral-critter-corral..."

TEST_DIR=$(mktemp -d)
echo "Temporary test directory: $TEST_DIR"

mkdir -p "$TEST_DIR/src"
cp tests/main.tf "$TEST_DIR/"
cp src/main.tf "$TEST_DIR/src/"
cp src/variables.tf "$TEST_DIR/src/"
cp src/outputs.tf "$TEST_DIR/src/"

# Mock rationale: Terraform init and validate are run against a local
# test configuration. No actual cloud resources are provisioned.
# The AWS provider is declared in tests/main.tf but its credentials
# are mocked, preventing actual API calls during `validate`.

cd "$TEST_DIR"

echo "Initializing Terraform..."
terraform init -backend=false # -backend=false ensures no remote state config is attempted

echo "Validating Terraform configuration..."
if ! terraform validate; then
  echo "Terraform validation failed!"
  exit 1
fi
echo "Terraform validation successful."

echo "All offline tests passed for nightly-ephemeral-critter-corral!"

# Cleanup
rm -rf "$TEST_DIR"
