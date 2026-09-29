#!/usr/bin/env bash
set -e
# Initialize Terraform without a remote backend (offline safe)
terraform init -backend=false -input=false > /dev/null
# Validate the configuration syntax
terraform validate
echo "Terraform validation passed."
