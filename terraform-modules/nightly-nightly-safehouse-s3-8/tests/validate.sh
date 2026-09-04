#!/usr/bin/env bash
set -e

# Navigate to module root (one level up from tests)
cd "$(dirname "$0")/.."

# Initialize Terraform without a backend (offline)
terraform init -backend=false > /dev/null

# Validate the configuration
terraform validate

echo "✅ Terraform module validation passed."
