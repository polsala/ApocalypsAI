#!/usr/bin/env bash
# Test script for nightly-apocalypse-safehouse-s3 Terraform module
# Runs offline – no AWS credentials required (provider skips validation)

set -euo pipefail

MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.. && pwd)"
cd "$MODULE_DIR"

# Initialize Terraform (skip backend to avoid remote state)
terraform init -backend=false -input=false > /dev/null

# Validate configuration syntax
terraform validate

# Generate a plan with sample variables
cat > test.tfvars <<'EOF'
bucket_name   = "test-safehouse-bucket"
region        = "us-east-1"
create_supply = true
supply_content = "Test supply content"
EOF

terraform plan -var-file=test.tfvars -out=plan.out > /dev/null

# Ensure the plan contains the expected resources
if ! terraform show -json plan.out | grep -q "aws_s3_bucket.safehouse"; then
  echo "ERROR: S3 bucket resource missing in plan"
  exit 1
fi

if ! terraform show -json plan.out | grep -q "aws_s3_bucket_object.supply"; then
  echo "ERROR: Supply object resource missing in plan"
  exit 1
fi

echo "All checks passed."
