#!/usr/bin/env bash

set -euo pipefail

# Ensure Terraform is available
if ! command -v terraform >/dev/null 2>&1; then
  echo "Terraform CLI not found. Please install Terraform to run tests." >&2
  exit 1
fi

# Initialize the module without a backend (offline mode)
terraform init -backend=false >/dev/null

# Validate the configuration
terraform validate

# Mock rationale: The test runs only local validation; no AWS calls are made, ensuring deterministic offline execution.

echo "All tests passed."

