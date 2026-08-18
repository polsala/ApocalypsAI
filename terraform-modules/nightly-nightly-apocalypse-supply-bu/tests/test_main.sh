#!/usr/bin/env bash
set -euo pipefail

# Initialize Terraform with a local (no‑remote) backend
terraform -chdir=../src init -backend=false > /dev/null

# Validate the configuration – this does not require AWS credentials
terraform -chdir=../src validate

echo "All tests passed."
