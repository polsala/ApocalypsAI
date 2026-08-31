#!/usr/bin/env bash
# Mock rationale: offline test using terraform validate without contacting AWS.
set -euo pipefail

# Create a temporary working directory
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "${TMPDIR}"
}
trap cleanup EXIT

# Copy module files into temp dir
cp -r . "${TMPDIR}/module"
cd "${TMPDIR}/module"

# Initialise Terraform with a null backend to avoid remote state calls
terraform init -backend=false > /dev/null

# Validate the configuration
terraform validate

# Run a dry‑run plan to ensure no syntax errors (no actual AWS calls)
terraform plan -input=false -no-color -out=plan.out > /dev/null

echo "✅ Terraform module validation passed"
