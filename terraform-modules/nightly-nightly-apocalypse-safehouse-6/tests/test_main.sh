#!/usr/bin/env bash
set -e

# Initialize Terraform without a remote backend
terraform -chdir=src init -backend=false -input=false > /dev/null

# Validate the configuration; will exit non‑zero on errors
terraform -chdir=src validate

echo "Terraform module validation passed."
