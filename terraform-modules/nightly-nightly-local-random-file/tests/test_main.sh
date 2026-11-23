#!/usr/bin/env bash
# Test script for nightly-local-random-file Terraform module
# Mock rationale: Uses only local providers; no external network calls.
set -e

MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
cd "$MODULE_DIR"

# Initialize Terraform without a backend (offline mode)
terraform init -backend=false > /dev/null

# Validate the configuration
terraform validate

# Run a plan with example variables; ensure it succeeds
terraform plan -input=false -var='filename=test.txt' -var='length=8' > /dev/null

echo "All Terraform checks passed."
