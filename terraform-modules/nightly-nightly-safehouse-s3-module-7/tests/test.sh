#!/usr/bin/env bash
set -e
# Initialize Terraform without a backend (offline validation only)
terraform init -backend=false > /dev/null
# Validate the configuration syntax
terraform validate -no-color
# If we reach this point, the test passes
echo "Terraform validation passed."
