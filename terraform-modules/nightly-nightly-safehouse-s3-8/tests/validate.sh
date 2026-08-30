#!/usr/bin/env bash
set -e

# Mock rationale: This test runs terraform init and validate in a temporary directory,
# using the local filesystem backend to avoid external calls.

TMPDIR=$(mktemp -d)
cp -r "$(dirname "$0")/../src" "$TMPDIR/module"
cd "$TMPDIR/module"

# Initialize without backend to keep offline
terraform init -backend=false > /dev/null

# Validate configuration
terraform validate

# Ensure expected resources are present
grep -q 'resource "aws_s3_bucket" "safehouse"' main.tf
grep -q 'versioning {' main.tf
grep -q 'noncurrent_version_expiration' main.tf

echo "All checks passed."
