#!/bin/bash
set -euo pipefail

# Mock rationale: This test script performs an offline validation of the Terraform module.
# It uses `terraform init -backend=false` to avoid connecting to a real backend,
# `terraform validate` for syntax checks, and `terraform plan` to generate an execution plan.
# The plan is then inspected using `terraform show -json` and `jq` to verify that the
# expected AWS resources (S3 bucket, Lambda, API Gateway) would be created with the correct names,
# without requiring any actual AWS credentials or provisioning real infrastructure.
# This ensures the module's structure and resource definitions are correct deterministically.

echo "--- Running Terraform module plan test ---"

TEMP_DIR=$(mktemp -d)
echo "Working in temporary directory: $TEMP_DIR"

# Copy module source to temp directory
cp -R src/* "$TEMP_DIR/"

# Create a test configuration file in the temp directory
cat <<EOF > "$TEMP_DIR/test.tf"
provider "aws" {
  region = "us-east-1"
  # Mock rationale: No actual AWS credentials are needed for terraform plan/validate.
  # The provider block is required for syntax, but its configuration is not used for offline checks.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "echo_chamber" {
  source = "./" # Reference the module in the current directory
  project_name = "test-apocalypsai"
  bucket_name_prefix = "test-echo-chamber"
  region = "us-east-1"
}

output "api_gateway_url" {
  value = module.echo_chamber.api_gateway_url
}

output "s3_bucket_name" {
  value = module.echo_chamber.s3_bucket_name
}
EOF

cd "$TEMP_DIR"

echo "Initializing Terraform..."
terraform init -backend=false > /dev/null # Mock rationale: Avoids real backend connection

echo "Validating Terraform configuration..."
terraform validate

echo "Generating Terraform plan..."
terraform plan -out=tfplan -var="project_name=test-apocalypsai" -var="bucket_name_prefix=test-echo-chamber" -var="region=us-east-1"

echo "Inspecting plan for expected resources..."
PLAN_JSON=$(terraform show -json tfplan)

# Check for S3 bucket
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.after.bucket == "test-echo-chamber-test-apocalypsai-echoes")' > /dev/null; then
  echo "ERROR: S3 bucket 'test-echo-chamber-test-apocalypsai-echoes' not found in plan."
  exit 1
fi
echo "S3 bucket found: test-echo-chamber-test-apocalypsai-echoes"

# Check for Lambda function
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_lambda_function" and .change.after.function_name == "test-apocalypsai-echo-chamber-handler")' > /dev/null; then
  echo "ERROR: Lambda function 'test-apocalypsai-echo-chamber-handler' not found in plan."
  exit 1
}
echo "Lambda function found: test-apocalypsai-echo-chamber-handler"

# Check for API Gateway
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_api_gateway_rest_api" and .change.after.name == "test-apocalypsai-EchoChamberAPI")' > /dev/null; then
  echo "ERROR: API Gateway 'test-apocalypsai-EchoChamberAPI' not found in plan."
  exit 1
}
echo "API Gateway found: test-apocalypsai-EchoChamberAPI"

echo "All expected resources found in plan. Test passed!"

# Clean up
cd - > /dev/null
rm -rf "$TEMP_DIR"
echo "Cleaned up temporary directory: $TEMP_DIR"
