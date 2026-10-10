#!/usr/bin/env bash
# Test that the Terraform module validates successfully.
# Mock rationale: we assume terraform is installed and AWS provider is available locally.

set -e

MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"

cd "$MODULE_DIR"

# Initialize without backend to keep it offline
terraform init -backend=false > /dev/null

# Validate the configuration
terraform validate

echo "Terraform module validation passed."
