#!/usr/bin/env bash
# Mock rationale: This script runs terraform init and validate in a deterministic offline mode.
set -e

# Initialize Terraform without a remote backend (local only)
terraform init -backend=false > /dev/null

# Validate the configuration; will exit non‑zero on errors
terraform validate

echo "Terraform validation passed."
