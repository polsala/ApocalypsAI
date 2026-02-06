#!/usr/bin/env bash
set -e

# Initialize Terraform without a remote backend (offline mode)
terraform init -backend=false > /dev/null

# Validate the configuration; will exit non‑zero on failure
terraform validate

echo "✅ Terraform configuration is valid."
