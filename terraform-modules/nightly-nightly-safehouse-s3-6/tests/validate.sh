#!/usr/bin/env bash
set -e

# Mock rationale: Assume terraform binary is available in PATH.
# Initialize the module without a backend.
terraform init -backend=false > /dev/null

# Validate the configuration.
terraform validate

echo "Terraform module validation passed."
