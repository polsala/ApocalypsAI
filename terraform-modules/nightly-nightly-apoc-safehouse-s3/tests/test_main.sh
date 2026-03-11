#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Use a temporary directory to isolate Terraform init and avoid external state.
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "${TMPDIR}"
}
trap cleanup EXIT

# Copy module files into temp dir
cp -r . "${TMPDIR}/module"
cd "${TMPDIR}/module"

# Initialize Terraform without a backend (local only)
terraform init -backend=false > /dev/null

# Validate configuration
terraform validate

# Run a plan with dummy input values (no interactive prompts)
terraform plan -input=false -out=plan.out \
  -var='bucket_name_prefix=apoc-test' \
  -var='versioning_enabled=true' \
  -var='lifecycle_days=7' > /dev/null

# Ensure the plan contains the aws_s3_bucket resource
if terraform show -json plan.out | grep -q '"type": "aws_s3_bucket"'; then
  echo "Test passed: aws_s3_bucket resource is present in the plan."
  exit 0
else
  echo "Test failed: aws_s3_bucket resource not found in the plan." >&2
  exit 1
fi
