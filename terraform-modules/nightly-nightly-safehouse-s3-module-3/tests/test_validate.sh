#!/usr/bin/env bash
set -e

# Mock rationale: This script runs terraform init (with local backend) and validate.
# It does not require any AWS credentials because no provider configuration is needed for validation.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"

# Initialize Terraform without backend to keep it offline
terraform init -backend=false > /dev/null

# Validate configuration
terraform validate

echo "✅ Terraform validation passed"
