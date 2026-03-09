#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Use local backend and dummy provider configuration; no real AWS calls.
# This test ensures Terraform configuration is syntactically valid.

# Initialize Terraform without remote backend
terraform init -backend=false > /dev/null

# Validate configuration
terraform validate

echo "Terraform configuration is valid."
