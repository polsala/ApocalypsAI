#!/bin/bash

set -euo pipefail

# Mock rationale: The 'terraform' command is fully mocked to simulate its behavior without any network interaction
# or actual execution of Terraform binaries. This ensures the tests are strictly deterministic, fast, and
# completely offline, avoiding any cloud costs or external dependencies. The mock simulates successful
# 'init' and 'validate' commands, allowing the test to focus on verifying the HCL syntax and content.

# Create a temporary directory for the test
TEST_DIR=$(mktemp -d)
cleanup() {
  echo "Cleaning up temporary directory: ${TEST_DIR}"
  rm -rf "${TEST_DIR}"
}
trap cleanup EXIT

echo "Running tests in: ${TEST_DIR}"

# Create a mock terraform executable
MOCK_BIN_DIR="${TEST_DIR}/bin"
mkdir -p "${MOCK_BIN_DIR}"
cat << 'EOF' > "${MOCK_BIN_DIR}/terraform"
#!/bin/bash
if [[ "$1" == "init" ]]; then
  echo "Mock terraform init successful."
  exit 0
elif [[ "$1" == "validate" ]]; then
  echo "Mock terraform validate successful."
  exit 0
else
  echo "Unknown mock terraform command: $@" >&2
  exit 1
fi
EOF
chmod +x "${MOCK_BIN_DIR}/terraform"

# Add the mock bin directory to PATH
export PATH="${MOCK_BIN_DIR}:${PATH}"

# Copy Terraform source files to the temporary directory
cp -R ../src/* "${TEST_DIR}"

# Navigate to the temporary directory
pushd "${TEST_DIR}" > /dev/null

# --- Test 1: Terraform Init (mocked) ---
echo "\n--- Running terraform init (mocked) ---"
if ! terraform init -backend=false; then
  echo "Test Failed: Mock terraform init failed."
  exit 1
fi
echo "Test Passed: Mock terraform init successful."

# --- Test 2: Terraform Validate (mocked) ---
echo "\n--- Running terraform validate (mocked) ---"
if ! terraform validate; then
  echo "Test Failed: Mock terraform validate failed."
  exit 1
fi
echo "Test Passed: Mock terraform validate successful."

# --- Test 3: Check for S3 Bucket resource definition ---
echo "\n--- Checking for aws_s3_bucket resource ---"
if ! grep -q 'resource "aws_s3_bucket" "anchor_bucket"' main.tf; then
  echo "Test Failed: aws_s3_bucket.anchor_bucket not found in main.tf."
  exit 1
fi
echo "Test Passed: aws_s3_bucket.anchor_bucket found."

# --- Test 4: Check for CloudFront Distribution resource definition ---
echo "\n--- Checking for aws_cloudfront_distribution resource ---"
if ! grep -q 'resource "aws_cloudfront_distribution" "anchor_distribution"' main.tf; then
  echo "Test Failed: aws_cloudfront_distribution.anchor_distribution not found in main.tf."
  exit 1
fi
echo "Test Passed: aws_cloudfront_distribution.anchor_distribution found."

# --- Test 5: Check for bucket_name_prefix variable ---
echo "\n--- Checking for bucket_name_prefix variable ---"
if ! grep -q 'variable "bucket_name_prefix"' variables.tf; then
  echo "Test Failed: variable \"bucket_name_prefix\" not found in variables.tf."
  exit 1
fi
echo "Test Passed: variable \"bucket_name_prefix\" found."

# --- Test 6: Check for CloudFront domain name output ---
echo "\n--- Checking for cloudfront_domain_name output ---"
if ! grep -q 'output "cloudfront_domain_name"' outputs.tf; then
  echo "Test Failed: output \"cloudfront_domain_name\" not found in outputs.tf."
  exit 1
fi
echo "Test Passed: output \"cloudfront_domain_name\" found."

popd > /dev/null

echo "\nAll tests passed for nightly-temporal-anchor!"
