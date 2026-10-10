#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Use a temporary directory to isolate Terraform init/plan.
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

# Copy module files into temp (excluding the test script itself)
cp -r ../* "$TMPDIR/"

cd "$TMPDIR"

# Initialize Terraform without a backend (offline safe)
terraform init -backend=false > /dev/null

# Validate configuration syntax
terraform validate

# Apply in plan mode to generate the password (no actual resources are created)
terraform apply -auto-approve -input=false -no-color > /dev/null

# Capture the generated password
PASS=$(terraform output -json password | tr -d '"')

# Test: ensure the password length matches the default variable (16)
if [ "${#PASS}" -ne 16 ]; then
  echo "Test failed: expected password length 16, got ${#PASS}"
  exit 1
fi

echo "All tests passed."
