#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests..."

# Navigate to the test directory
cd "$(dirname "$0")"

# Initialize Terraform in the test directory.
# -backend=false prevents Terraform from trying to configure a state backend,
# making the init process faster and suitable for offline validation.
# Mock rationale: We are not deploying, only validating configuration. This step
# downloads necessary provider plugins. For strict offline execution after the first run,
# ensure plugins are cached in the .terraform directory.
terraform init -backend=false

# Validate the Terraform configuration.
# This checks syntax, variable definitions, and provider configurations without
# needing to connect to the cloud provider or fetch real resource data.
# It's a purely offline, deterministic check.
echo "Running terraform validate..."
terraform validate

echo "Terraform module tests passed successfully!"
