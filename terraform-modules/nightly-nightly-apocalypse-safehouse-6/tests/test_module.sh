#!/usr/bin/env bash
# Mock rationale: This test runs only local Terraform commands (init & validate) without contacting AWS.
set -e

MODULE_DIR="$(cd $(dirname $0)/.. && pwd)"
cd "$MODULE_DIR"

# Initialise Terraform without a backend (offline only)
terraform init -backend=false > /dev/null

# Validate the configuration
terraform validate

echo "✅ Terraform module validation passed."
