#!/usr/bin/env bash
# Test script for nightly-apocalypse-safehouse-s3 Terraform module
# Mock rationale: This script runs entirely offline using the local backend.

set -euo pipefail

# Ensure Terraform is available
if ! command -v terraform >/dev/null 2>&1; then
  echo "Terraform CLI not found. Install Terraform to run tests."
  exit 1
fi

# Create a temporary working directory
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "${TMPDIR}"
}
trap cleanup EXIT

# Copy module files into temp dir
cp -r . "${TMPDIR}/module"
cd "${TMPDIR}/module"

# Initialize Terraform with local backend (no remote state)
terraform init -backend=false -input=false >/dev/null

# Validate configuration
terraform validate

# Generate a plan (no apply)
terraform plan -input=false -out=plan.out >/dev/null

# Ensure the plan contains the expected resource
if terraform show -json plan.out | grep -q '"type": "aws_s3_bucket"'; then
  echo "✅ Plan contains aws_s3_bucket.safehouse"
  exit 0
else
  echo "❌ Expected aws_s3_bucket.safehouse not found in plan"
  exit 1
fi
