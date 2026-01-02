#!/usr/bin/env bash
set -euo pipefail

# Initialise the module without a remote backend (offline only)
terraform -chdir=../src init -backend=false > /dev/null

# Validate the configuration – this does not require AWS credentials
terraform -chdir=../src validate

echo "Terraform validation succeeded."
