#!/usr/bin/env bash
# Mock rationale: This script runs terraform init and validate to ensure the module syntax is correct.
set -e

# Create a temporary working directory
TMPDIR=$(mktemp -d)
cp -R . "$TMPDIR/module"
cd "$TMPDIR/module"

terraform init -backend=false > /dev/null 2>&1
terraform validate

echo "✅ Terraform module validation passed."
