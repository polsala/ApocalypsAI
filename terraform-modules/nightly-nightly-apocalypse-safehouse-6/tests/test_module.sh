#!/usr/bin/env bash
set -e

# Navigate to the module source directory
cd "$(dirname "$0")/../src"

# Initialise Terraform without a backend (offline safe mode)
terraform init -backend=false > /dev/null

# Validate the configuration syntax
terraform validate

if [ $? -eq 0 ]; then
  echo "PASS: terraform validate succeeded"
else
  echo "FAIL: terraform validate failed"
  exit 1
fi
