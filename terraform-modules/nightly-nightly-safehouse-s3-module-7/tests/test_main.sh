#!/usr/bin/env bash
set -e

# Initialize Terraform (no backend) # Mock rationale: avoids remote state, keeps test offline
terraform init -backend=false > /dev/null

# Validate the configuration syntax
terraform validate

# Create a temporary tfvars file with mock inputs
cat > terraform.tfvars <<EOF
bucket_name = "test-safehouse-bucket"
tags = {
  Environment = "test"
}
EOF

# Generate a plan using the mock variables
terraform plan -var-file=terraform.tfvars -out=plan.out > /dev/null

# Verify that the plan contains the expected resources using JSON output
PLAN_JSON=$(terraform show -json plan.out)

if ! echo "$PLAN_JSON" | grep -q '"aws_s3_bucket"'; then
  echo "Missing aws_s3_bucket resource"
  exit 1
fi

if ! echo "$PLAN_JSON" | grep -q '"aws_s3_bucket_versioning"'; then
  echo "Missing versioning configuration"
  exit 1
fi

if ! echo "$PLAN_JSON" | grep -q '"aws_s3_bucket_server_side_encryption_configuration"'; then
  echo "Missing encryption configuration"
  exit 1
fi

if ! echo "$PLAN_JSON" | grep -q '"aws_s3_bucket_lifecycle_configuration"'; then
  echo "Missing lifecycle configuration"
  exit 1
fi

if ! echo "$PLAN_JSON" | grep -q '"aws_iam_policy"'; then
  echo "Missing IAM policy"
  exit 1
fi

echo "All checks passed"
