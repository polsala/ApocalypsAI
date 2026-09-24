#!/usr/bin/env bash
set -e
# Initialize Terraform without remote backend (offline deterministic)
terraform init -backend=false > /dev/null
# Validate configuration syntax and provider requirements
terraform validate
echo "Validation successful."
