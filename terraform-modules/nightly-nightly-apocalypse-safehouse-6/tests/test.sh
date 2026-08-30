#!/usr/bin/env bash
set -e

# Initialise Terraform with a local (no‑backend) configuration
terraform -chdir=../src init -backend=false > /dev/null

# Validate the configuration – should succeed without contacting AWS
terraform -chdir=../src validate

echo "All tests passed."
