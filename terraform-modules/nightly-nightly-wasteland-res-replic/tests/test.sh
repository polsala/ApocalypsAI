#!/bin/bash
set -euo pipefail

echo "--- Running Terraform module tests ---"

# Change to the test directory
cd "$(dirname "$0")"

# Initialize Terraform (offline for null_resource)
echo "Initializing Terraform..."
terraform init -backend=false -input=false

# Mock rationale:
# For `null_resource`, `terraform init` does not require actual cloud provider credentials
# or network access, making it suitable for offline testing. The `local-exec` provisioners
# are not executed during `init` or `validate`, only during `apply`/`destroy`.
# The `-backend=false` flag ensures no remote state backend is configured, keeping it local.

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Mock rationale:
# `terraform validate` performs syntax checks, verifies variable definitions,
# and ensures module calls are correct without needing to interact with any
# cloud provider APIs. This makes it a deterministic and offline test.

if [ $? -eq 0 ]; then
  echo "Terraform validation successful!"
  echo "--- Test Passed ---"
  exit 0
else
  echo "Terraform validation failed!"
  echo "--- Test Failed ---"
  exit 1
fi
