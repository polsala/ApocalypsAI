#!/bin/bash

# Mock rationale: This script performs offline validation of the Terraform module.
# It does not require actual cloud credentials or network access beyond
# fetching provider plugins during 'terraform init' (which can be cached).
# The 'validate' command checks HCL syntax and configuration logic.

set -e

echo "--- Running offline Terraform module tests ---"

# Navigate to the test directory
cd "$(dirname "$0")"

echo "Initializing Terraform..."
# terraform init will download providers. For truly offline, one would pre-download.
# For this context, 'offline' means no actual cloud API calls for validation.
terraform init -backend=false -plugin-dir=./.terraform/plugins # Mock rationale: -backend=false prevents state backend config, -plugin-dir can point to pre-downloaded plugins for full offline.

echo "Validating Terraform configuration..."
terraform validate

echo "--- Terraform module tests passed successfully! ---"
