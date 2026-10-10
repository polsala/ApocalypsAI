#!/usr/bin/env bash
set -e

# Initialize the module without a remote backend
terraform -chdir=../src init -backend=false > /dev/null

# Validate the configuration
terraform -chdir=../src validate

echo "Terraform module validation passed."
