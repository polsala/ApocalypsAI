#!/usr/bin/env bash
# Test script for nightly-safehouse-s3-module
# Mock rationale: runs terraform locally without contacting AWS; validates configuration only.
set -e

# Ensure terraform is available
if ! command -v terraform >/dev/null 2>&1; then
  echo "Terraform CLI not found. Skipping test."
  exit 0
fi

# Create a temporary working directory
TMPDIR=$(mktemp -d)
cp -r ../* "$TMPDIR/"
cd "$TMPDIR"

# Initialize without a backend (offline)
terraform init -backend=false -input=false >/dev/null

# Validate the configuration
if terraform validate >/dev/null; then
  echo "✅ terraform validate passed"
  exit 0
else
  echo "❌ terraform validate failed"
  exit 1
fi
