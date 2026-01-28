#!/usr/bin/env bash
set -e

# Mock rationale: Use a temporary directory to run terraform commands without affecting the repo.
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

# Copy module files into the temporary directory
cp -r "$(dirname "$0")/../src" "$TMPDIR/module"

cd "$TMPDIR/module"

# Initialize Terraform without a backend (offline mode)
terraform init -backend=false -input=false > /dev/null

# Validate the configuration syntax
terraform validate

# Provide dummy AWS credentials for a dry‑run plan (no real calls are made)
export AWS_ACCESS_KEY_ID="test"
export AWS_SECRET_ACCESS_KEY="test"
export AWS_DEFAULT_REGION="us-east-1"

# Perform a plan; errors will cause the script to exit due to set -e
terraform plan -input=false -lock=false -no-color -out=plan.out > /dev/null

echo "All tests passed."
