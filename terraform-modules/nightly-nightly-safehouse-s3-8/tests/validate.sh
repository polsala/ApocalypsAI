#!/usr/bin/env bash
set -e
# Mock rationale: This script runs terraform validate without contacting any remote services.
# Initialise Terraform without a backend to keep the test self‑contained.
terraform init -backend=false > /dev/null
# Validate the configuration; will exit with non‑zero if there are errors.
terraform validate
echo "Terraform validation passed."
