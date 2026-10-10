#!/usr/bin/env bash
set -euo pipefail

# Determine the directory containing the Terraform module
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"

cd "$MODULE_DIR"

# Initialize Terraform without a remote backend (offline mode)
terraform init -backend=false > /dev/null

# Validate the configuration; will exit non‑zero on errors
terraform validate

echo "Terraform validation passed."
