#!/usr/bin/env bash
set -euo pipefail

# Initialize the module in a temporary directory
WORKDIR=$(mktemp -d)
cp -R "$(dirname "$0")/.." "$WORKDIR/module"
cd "$WORKDIR/module"

# Mock rationale: Use local backend to avoid remote state and external calls.
terraform init -backend=false > /dev/null

# Validate syntax
terraform validate

# Generate a plan without applying
terraform plan -input=false -out=plan.out > /dev/null

# Ensure the plan contains the S3 bucket resource
if ! grep -q 'aws_s3_bucket.safehouse' plan.out; then
  echo "Test failed: S3 bucket resource not found in plan"
  exit 1
fi

echo "All tests passed."
