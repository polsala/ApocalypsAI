#!/usr/bin/env bash
set -e

# Initialize Terraform without a backend (offline test)
terraform init -backend=false > /dev/null

# Validate the configuration
terraform validate

echo "✅ Terraform module validation passed"
