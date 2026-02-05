#!/usr/bin/env bash
# Mock rationale: This script runs terraform init with -backend=false to avoid remote state,
# then validates the configuration. No external calls are made, making it deterministic.

set -e

# Initialize Terraform without backend
terraform init -backend=false > /dev/null

# Validate configuration
terraform validate

echo "✅ Terraform module validation passed."
