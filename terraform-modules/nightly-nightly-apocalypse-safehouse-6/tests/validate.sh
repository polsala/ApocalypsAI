#!/usr/bin/env bash
# Mock rationale: This script runs terraform init and validate in a temporary directory.
# It does not contact any real AWS endpoints because -backend=false disables remote state.
# The test passes if terraform exits with status 0.

set -euo pipefail

# Create a temporary working directory
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "${TMPDIR}"
}
trap cleanup EXIT

# Copy module files into the temp dir
cp -r ../* "${TMPDIR}/"

# Change to temp dir
cd "${TMPDIR}"

# Initialize Terraform (no backend) and validate
terraform init -backend=false > /dev/null
terraform validate

echo "✅ Terraform configuration validated successfully."
