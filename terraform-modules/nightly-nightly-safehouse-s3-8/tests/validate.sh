#!/usr/bin/env bash
set -euo pipefail

# Initialize Terraform without a remote backend (keeps everything local)
terraform init -backend=false > /dev/null

# Validate the configuration – will exit non‑zero on errors
terraform validate

# If we get here, validation succeeded
echo "Terraform configuration is valid."
