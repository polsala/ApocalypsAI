#!/usr/bin/env bash
set -euo pipefail

# Navigate to the module root (one level up from tests)
cd "$(dirname "$0")/.."

# Initialize Terraform without a backend (offline safe)
terraform init -backend=false > /dev/null

# Validate the configuration; will exit non‑zero on errors
terraform validate

echo "✅ Terraform configuration is valid."
