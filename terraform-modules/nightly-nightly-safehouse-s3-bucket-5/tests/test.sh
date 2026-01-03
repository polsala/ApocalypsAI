#!/usr/bin/env bash
set -e

# Initialize Terraform without remote backend (offline safe)
terraform init -backend=false > /dev/null

# Validate the configuration syntax and provider blocks
terraform validate

echo "All tests passed."
