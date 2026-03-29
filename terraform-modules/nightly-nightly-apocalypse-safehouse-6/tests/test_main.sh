#!/usr/bin/env bash
set -e

# Mock rationale: Use a temporary directory to avoid polluting the repo.
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

# Copy module files into temp dir
cp -r . "$TMPDIR/module"
cd "$TMPDIR/module"

# Initialize Terraform without a backend (offline test)
terraform init -backend=false > /dev/null

# Validate configuration syntax
terraform validate

# Run a plan with dummy variable to ensure no runtime errors
terraform plan -input=false -var "bucket_name=test-safehouse-bucket-$(date +%s)" -out=plan.out > /dev/null

echo "✅ Terraform module passed validation and plan steps."
