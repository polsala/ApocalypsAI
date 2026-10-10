#!/bin/bash
set -euo pipefail

echo "--- Running Terraform module tests for Nightly Chrono-Vault ---"

# Mock rationale:
# 1. 'terraform init -backend=false': Initializes the test configuration
#    without configuring a state backend, making it deterministic and offline.
#    It downloads necessary provider schemas locally.
# 2. 'terraform fmt --check': Ensures consistent code formatting.
# 3. 'terraform validate': Checks the module's syntax, variable definitions,
#    and overall configuration validity against the downloaded provider schemas,
#    without making any actual cloud API calls. This ensures the module is
#    syntactically correct and adheres to provider requirements.

TEST_CONFIG_DIR="tests/test_config"
MODULE_SRC_DIR="src"

# Ensure the test config directory exists
mkdir -p "${TEST_CONFIG_DIR}"

echo "Navigating to test configuration directory: ${TEST_CONFIG_DIR}"
cd "${TEST_CONFIG_DIR}"

echo "Running terraform init -backend=false..."
# This will download the AWS provider plugin into .terraform/plugins,
# allowing subsequent validate commands to work offline.
# -backend=false prevents configuring a remote state backend.
terraform init -backend=false
if [ $? -ne 0 ]; then
  echo "Terraform init failed."
  exit 1
fi
echo "Terraform init passed."

echo "Running terraform fmt --check..."
terraform fmt --check .
if [ $? -ne 0 ]; then
  echo "Terraform formatting check failed. Run 'terraform fmt' in '${TEST_CONFIG_DIR}' to fix."
  exit 1
fi
echo "Terraform formatting check passed."

echo "Running terraform validate..."
terraform validate .
if [ $? -ne 0 ]; then
  echo "Terraform validation failed."
  exit 1
fi
echo "Terraform validation passed."

echo "--- All Nightly Chrono-Vault tests passed! ---"
