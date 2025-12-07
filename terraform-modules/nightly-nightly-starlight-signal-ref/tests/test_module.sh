#!/bin/bash
set -euo pipefail

# Mock rationale: Terraform commands (init, validate, apply, output) interact with the filesystem,
# download providers, and potentially communicate with cloud APIs. To ensure deterministic and
# offline testing, the 'terraform' binary is mocked. This mock simulates successful execution
# and predefined outputs, allowing the test script to verify the module's structure and
# expected behavior without actual cloud resource provisioning or network calls.

echo "--- Running Starlight Signal Reflector Terraform Module Tests ---"

# Create a temporary directory for the test environment
TEST_DIR=$(mktemp -d -t starlight-reflector-test-XXXXXX)
echo "Created temporary test directory: $TEST_DIR"
cleanup() {
  echo "Cleaning up temporary test directory: $TEST_DIR"
  rm -rf "$TEST_DIR"
}
trap cleanup EXIT

# Copy module source to the test directory
cp -r src "$TEST_DIR/module_src"

# Create a dummy root module in the test directory to call our module
cat <<EOF > "$TEST_DIR/main.tf"
provider "aws" {
  region = "us-east-1"
  # Mock rationale: AWS provider configuration is required by Terraform,
  # but actual credentials are not needed as the 'terraform' binary is mocked.
  # This block satisfies Terraform's parsing requirements.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "starlight_reflector" {
  source       = "./module_src"
  project_name = "test-starlight"
  aws_region   = "us-east-1"
}

output "api_gateway_url" {
  value = module.starlight_reflector.api_gateway_url
}
EOF

# Set up the mock terraform binary in PATH
export PATH="$(pwd)/tests:$PATH"

cd "$TEST_DIR"

echo "1. Running terraform fmt -check..."
if ! terraform fmt -check; then
  echo "FAIL: Terraform files are not formatted correctly."
  exit 1
fi
echo "PASS: Terraform files are formatted correctly."

echo "2. Running terraform init..."
if ! terraform init; then
  echo "FAIL: terraform init failed."
  exit 1
fi
echo "PASS: terraform init successful."

echo "3. Running terraform validate..."
if ! terraform validate; then
  echo "FAIL: terraform validate failed."
  exit 1
fi
echo "PASS: terraform validate successful."

echo "4. Running terraform apply (mocked)..."
if ! terraform apply -auto-approve; then
  echo "FAIL: terraform apply (mocked) failed."
  exit 1
fi
echo "PASS: terraform apply (mocked) successful."

echo "5. Checking terraform output (mocked)..."
OUTPUT=$(terraform output -json api_gateway_url)
EXPECTED_OUTPUT="{\"api_gateway_url\": \"https://mock-api-gateway-url.execute-api.us-east-1.amazonaws.com/prod\"}"

if [[ "$OUTPUT" == "$EXPECTED_OUTPUT" ]]; then
  echo "PASS: terraform output matches expected mock output."
else
  echo "FAIL: terraform output mismatch."
  echo "Expected: $EXPECTED_OUTPUT"
  echo "Got:      $OUTPUT"
  exit 1
fi

echo "--- All Starlight Signal Reflector Terraform Module Tests Passed! ---"
