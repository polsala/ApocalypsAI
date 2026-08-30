#!/usr/bin/env bash
set -e

# Navigate to the module directory (assumes script is run from the module root)
# Initialize Terraform without a backend to avoid remote calls.
terraform init -backend=false > /dev/null

# Validate the configuration. This checks syntax and provider requirements without contacting AWS.
terraform validate

echo "Terraform validation passed"
