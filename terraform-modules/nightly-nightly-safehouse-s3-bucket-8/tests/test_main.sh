#!/usr/bin/env bash
# test_main.sh – validates the nightly‑safehouse‑s3‑bucket Terraform module
# Mock rationale: This test runs entirely offline; it only checks that the configuration
# parses and contains the expected AWS S3 bucket resource.

set -euo pipefail

# Ensure Terraform is available
if ! command -v terraform >/dev/null 2>&1; then
  echo "Terraform not found in PATH – skipping test."
  exit 0
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

# Write a minimal root configuration that uses the module
cat > main.tf <<'EOF'
module "test_safehouse" {
  source            = "./src"
  bucket_name       = "test‑bucket‑12345"
  enable_encryption = false
}
EOF

# Initialise Terraform (backend disabled for speed)
terraform init -backend=false >/dev/null

# Validate configuration – should exit with 0 if syntax is correct
if ! terraform validate >/dev/null; then
  echo "Terraform validation failed"
  exit 1
fi

# Ensure the plan contains the aws_s3_bucket resource
PLAN_OUTPUT=$(terraform plan -no-color -input=false 2>/dev/null || true)
if echo "$PLAN_OUTPUT" | grep -q "aws_s3_bucket.safehouse"; then
  echo "Test passed: aws_s3_bucket resource found in plan."
  exit 0
else
  echo "Test failed: aws_s3_bucket resource not found in plan."
  exit 1
fi
