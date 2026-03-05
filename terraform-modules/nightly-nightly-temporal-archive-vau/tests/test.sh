#!/bin/bash

set -euo pipefail

echo "Running Terraform validation tests..."

# Change to the tests directory
cd "$(dirname "$0")"

# Clean up previous runs' artifacts for a deterministic test environment
rm -rf .terraform .terraform.lock.hcl terraform.tfstate*

# Initialize Terraform (downloads providers if not cached, then runs locally)
# Mock rationale: `terraform init` requires network access to download necessary providers
# (e.g., hashicorp/aws). Once downloaded, subsequent `terraform validate` commands
# can run offline. For a truly offline *first-time* run, providers would need to be
# pre-cached in the system's Terraform plugin directory. This test assumes `init`
# can complete its provider download phase, making the `validate` step offline.
echo "Attempting terraform init (may require network for initial provider download)..."
terraform init -backend=false # -backend=false prevents state backend configuration, focusing on module validation.
if [ $? -ne 0 ]; then
  echo "ERROR: Terraform init failed."
  exit 1
fi
echo "SUCCESS: Terraform init completed."

echo "Validating module configuration..."
terraform validate -json > /dev/null
if [ $? -ne 0 ]; then
  echo "ERROR: Terraform validation failed for the module configurations."
  exit 1
fi
echo "SUCCESS: All module configurations validated."

# Clean up artifacts after test
rm -rf .terraform .terraform.lock.hcl terraform.tfstate*

echo "All Terraform validation tests passed!"
