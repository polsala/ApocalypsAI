#!/bin/bash
set -euo pipefail

# Mock rationale: This test is deterministic and offline.
# It validates Terraform syntax and structure without requiring AWS credentials
# or actual resource provisioning. `terraform validate` checks HCL syntax.
# `terraform plan -no-color` generates a plan output that can be inspected
# for expected resource types, simulating a dry run.

echo "--- Running Terraform module tests ---"

MODULE_DIR="../src"
TEST_TEMP_DIR="./temp_test_env"

# Clean up previous test environment
rm -rf "${TEST_TEMP_DIR}"
mkdir -p "${TEST_TEMP_DIR}"
cd "${TEST_TEMP_DIR}"

# Create a dummy main.tf for testing the module
cat <<EOF > main.tf
provider "aws" {
  region = "us-east-1"
  # Mock rationale: For plan validation, a dummy provider config is sufficient.
  # No actual AWS calls are made by 'terraform validate' or 'terraform plan'
  # when checking syntax and resource graph.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "test_echo_chamber" {
  source = "${MODULE_DIR}"

  bucket_name_prefix = "test-echo"
  content_html       = "<h1>Test Echo!</h1>"
  tags = {
    Test = "True"
  }
}
EOF

echo "Initializing Terraform..."
terraform init -backend=false # Mock rationale: No actual backend needed for validation/plan
if [ $? -ne 0 ]; then
  echo "Terraform init failed!"
  exit 1
fi
echo "Terraform init successful."

echo "Validating Terraform configuration..."
terraform validate
if [ $? -ne 0 ]; then
  echo "Terraform validation failed!"
  exit 1
fi
echo "Terraform validation successful."

echo "Generating Terraform plan (dry run)..."
PLAN_OUTPUT=$(terraform plan -no-color -input=false -out=tfplan)
if [ $? -ne 0 ]; then
  echo "Terraform plan generation failed!"
  exit 1
fi
echo "Terraform plan generated."

# Inspect the plan output for expected resources
echo "Inspecting plan for expected resources..."

# Check for S3 bucket
if ! grep -q "aws_s3_bucket.echo_chamber_bucket" <<< "${PLAN_OUTPUT}"; then
  echo "Error: S3 bucket resource not found in plan."
  exit 1
fi

# Check for CloudFront distribution
if ! grep -q "aws_cloudfront_distribution.echo_chamber_cdn" <<< "${PLAN_OUTPUT}"; then
  echo "Error: CloudFront distribution resource not found in plan."
  exit 1
fi

# Check for S3 object (index.html)
if ! grep -q "aws_s3_object.index_html" <<< "${PLAN_OUTPUT}"; then
  echo "Error: S3 object (index.html) resource not found in plan."
  exit 1
fi

echo "All expected resources found in plan."

echo "--- All Terraform module tests passed! ---"

# Clean up
cd - > /dev/null # Go back to original directory
rm -rf "${TEST_TEMP_DIR}"
