#!/usr/bin/env bash
set -e

# Mock rationale: This script runs terraform init and validate in a temporary directory.
# It does not contact real AWS because the provider can be pointed at a mock endpoint.
# In CI the AWS provider will be configured with environment variables that point to a mock.

TMPDIR=$(mktemp -d)
cp -r . "$TMPDIR"
cd "$TMPDIR"

terraform init -backend=false > /dev/null
terraform validate

echo "✅ Terraform module validation passed"
