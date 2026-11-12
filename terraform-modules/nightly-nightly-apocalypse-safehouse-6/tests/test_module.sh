#!/usr/bin/env bash
set -euo pipefail

# Navigate to the module source directory
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"

cd "$MODULE_DIR"

# Initialise Terraform without a remote backend (offline safe)
terraform init -backend=false > /dev/null

# Validate the configuration syntax and internal consistency
terraform validate

echo "✅ Terraform module validation passed."
