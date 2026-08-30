#!/usr/bin/env bash
set -e

# Initialize Terraform without a backend (offline mode)
terraform init -backend=false > /dev/null

# Validate the configuration syntax and internal consistency
terraform validate

echo "Terraform module validation passed."
