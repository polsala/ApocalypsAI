#!/usr/bin/env bash
set -e

# Initialize Terraform with a local (in‑memory) backend; no remote state needed
terraform -chdir=../src init -backend=false > /dev/null

# Validate the configuration syntax and provider blocks
terraform -chdir=../src validate

# Perform a dry‑run plan to ensure resources can be instantiated without errors
terraform -chdir=../src plan -input=false -out=plan.out > /dev/null

echo "All Terraform checks passed."
