#!/usr/bin/env bash
set -e

# Initialize Terraform without a remote backend (offline)
terraform init -backend=false > /dev/null

# Validate the configuration; will exit non‑zero on errors
terraform validate

echo "All tests passed."
