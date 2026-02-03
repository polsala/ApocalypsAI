#!/usr/bin/env bash
# Mock rationale: This script runs terraform commands in a temporary directory.
# It ensures the module syntax is valid without contacting AWS.
set -euo pipefail

# Create a temporary working directory
TMPDIR=$(mktemp -d)
cp -r $(dirname "$0")/../src/* "$TMPDIR/"
cd "$TMPDIR"

# Initialize Terraform with a local backend (no remote state)
export TF_IN_AUTOMATION=1
terraform init -backend=false > /dev/null

# Validate the configuration
terraform validate

# If we reach this point, the test passes
echo "✅ Terraform module validation succeeded"
