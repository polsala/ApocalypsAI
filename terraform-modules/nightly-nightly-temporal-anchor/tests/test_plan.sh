#!/bin/bash
set -euo pipefail

# Mock rationale: This test runs 'terraform plan' in an isolated, offline manner
# to verify the module's syntax and expected resource creation without
# interacting with actual AWS APIs. It uses dummy AWS credentials and
# a null backend to ensure determinism and avoid real cloud costs/side effects.

echo "--- Running Terraform Plan Test for Nightly Temporal Anchor ---"

# Create a temporary directory for the test
TEST_DIR=$(mktemp -d)
cp -r src/* "$TEST_DIR/"

# Define a test configuration that uses the module
cat <<EOF > "$TEST_DIR/main.tf"
provider "aws" {
  region = "us-east-1"
  # Mock rationale: Dummy credentials to satisfy Terraform provider requirements
  # without needing actual valid credentials for 'terraform plan'.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
  token      = "mock_session_token"
}

module "temporal_anchor_test" {
  source = "./" # Refer to the module in the current directory (TEST_DIR)

  bucket_name    = "test-temporal-anchor-bucket-12345"
  index_document = "affirmations.html"
  error_document = "temporal_rift.html"
}

output "test_s3_endpoint" {
  value = module.temporal_anchor_test.s3_website_endpoint
}

output "test_cloudfront_domain" {
  value = module.temporal_anchor_test.cloudfront_domain_name
}
EOF

cd "$TEST_DIR"

# Initialize Terraform with a null backend to prevent state file operations
# Mock rationale: -backend=false ensures no remote state interaction, making the test offline.
terraform init -backend=false > /dev/null

# Run terraform plan and capture output
PLAN_OUTPUT=$(terraform plan -no-color -input=false)
PLAN_EXIT_CODE=$?

if [ "$PLAN_EXIT_CODE" -ne 0 ]; then
  echo "Terraform plan failed with exit code $PLAN_EXIT_CODE"
  echo "$PLAN_OUTPUT"
  exit 1
fi

echo "Terraform plan successful. Verifying resources..."

# Verify expected resources are planned for creation
# Mock rationale: Grepping for resource types and names in the plan output
# confirms the module's configuration correctly defines these resources.
if ! echo "$PLAN_OUTPUT" | grep -q 'aws_s3_bucket.temporal_anchor_bucket'; then
  echo "Error: aws_s3_bucket.temporal_anchor_bucket not found in plan."
  exit 1
fi

if ! echo "$PLAN_OUTPUT" | grep -q 'aws_s3_bucket_policy.temporal_anchor_bucket_policy'; then
  echo "Error: aws_s3_bucket_policy.temporal_anchor_bucket_policy not found in plan."
  exit 1
fi

if ! echo "$PLAN_OUTPUT" | grep -q 'aws_cloudfront_origin_access_identity.temporal_anchor_oai'; then
  echo "Error: aws_cloudfront_origin_access_identity.temporal_anchor_oai not found in plan."
  exit 1
fi

if ! echo "$PLAN_OUTPUT" | grep -q 'aws_cloudfront_distribution.temporal_anchor_cdn'; then
  echo "Error: aws_cloudfront_distribution.temporal_anchor_cdn not found in plan."
  exit 1
fi

# Verify specific properties or outputs if possible from plan output
# For outputs, we can't directly get their *final* value from plan without apply,
# but we can check if they are *known after apply*.
if ! echo "$PLAN_OUTPUT" | grep -q 'test_s3_endpoint = (known after apply)'; then
  echo "Error: Output 'test_s3_endpoint' not found or not 'known after apply'."
  exit 1
fi

if ! echo "$PLAN_OUTPUT" | grep -q 'test_cloudfront_domain = (known after apply)'; then
  echo "Error: Output 'test_cloudfront_domain' not found or not 'known after apply'."
  exit 1
fi

echo "All expected resources and outputs found in plan."
echo "--- Test Passed ---"

# Clean up temporary directory
rm -rf "$TEST_DIR"
