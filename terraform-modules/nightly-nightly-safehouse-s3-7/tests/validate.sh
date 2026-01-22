#!/usr/bin/env bash
set -euo pipefail

# Initialize Terraform without a backend (offline test)
terraform -chdir=../src init -backend=false > /dev/null

# Validate configuration
terraform -chdir=../src validate

echo "Terraform configuration is valid."
