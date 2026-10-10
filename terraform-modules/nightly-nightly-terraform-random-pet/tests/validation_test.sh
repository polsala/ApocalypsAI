#!/usr/bin/env bash
set -e

# Initialize Terraform without configuring a backend (offline validation only)
terraform init -backend=false > /dev/null

# Validate the configuration; will exit non‑zero on errors
terraform validate

echo "Terraform module validation passed."
