#!/usr/bin/env bash
set -e

# Initialize Terraform without a remote backend (local only)
terraform -chdir=.. init -backend=false > /dev/null

# Validate the configuration syntax and internal consistency
terraform -chdir=.. validate

echo "Terraform configuration is valid."
