#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Use local backend and validate syntax without contacting AWS.
# Initialize Terraform without backend to avoid remote state.
terraform -chdir=../src init -backend=false > /dev/null

# Validate the configuration.
terraform -chdir=../src validate

echo "✅ Terraform configuration is valid."
