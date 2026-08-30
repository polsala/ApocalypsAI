#!/usr/bin/env bash
set -e

# Mock rationale: Use local backend to avoid real AWS calls.
# Initialize Terraform with a temporary directory.
TMPDIR=$(mktemp -d)
cp -R . "$TMPDIR/module"
cd "$TMPDIR/module"

# Write a minimal backend config to local.
cat > backend.tf <<'EOF'
terraform {
  backend "local" {}
}
EOF

terraform init -input=false > /dev/null

# Validate configuration
terraform validate

# Generate a plan with dummy values (no actual provider calls)
terraform plan -input=false -out=plan.out -var 'bucket_name=test-safehouse-bucket' > /dev/null

# Ensure plan contains expected resources
if ! terraform show -json plan.out | grep -q '"type":"aws_s3_bucket"'; then
  echo "Expected aws_s3_bucket resource not found in plan"
  exit 1
fi

echo "All tests passed."
