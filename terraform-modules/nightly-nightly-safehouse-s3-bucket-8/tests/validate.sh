#!/usr/bin/env bash
set -e

# Initialize Terraform without a remote backend to keep the test offline
terraform -chdir=../src init -backend=false > /dev/null

# Validate the configuration syntax
terraform -chdir=../src validate

echo "✅ Terraform module validation passed"
