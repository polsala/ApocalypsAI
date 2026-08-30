#!/usr/bin/env bash
set -e
# Initialise the module without a backend (no remote state needed for validation)
terraform init -backend=false > /dev/null
# Validate the configuration syntax and provider requirements
terraform validate
echo "All tests passed."
