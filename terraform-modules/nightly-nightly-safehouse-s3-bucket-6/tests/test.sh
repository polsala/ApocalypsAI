#!/usr/bin/env bash
set -e

# Move to the module root (parent directory of tests)
cd "$(dirname "$0")/.."

# Initialise Terraform without a backend (offline friendly)
terraform init -backend=false > /dev/null

# Validate the configuration – should succeed without contacting any cloud provider
terraform validate

echo "All tests passed."
