#!/usr/bin/env bash
set -e

# Initialize the module without a remote backend
terraform -chdir=src init -backend=false > /dev/null

# Validate the configuration syntax and provider requirements
terraform -chdir=src validate

echo "All Terraform checks passed."
