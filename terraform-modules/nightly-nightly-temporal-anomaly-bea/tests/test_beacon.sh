#!/bin/bash
set -euo pipefail

# Mock rationale: This test validates the Terraform module's syntax and structure
# without requiring actual AWS credentials or deploying resources.
# It uses 'terraform init -backend=false' to avoid needing a real state backend
# and 'terraform validate' to check the configuration.

echo "Running offline Terraform module validation test..."

TEST_DIR=$(mktemp -d)
trap "rm -rf $TEST_DIR" EXIT

echo "Creating temporary test environment in $TEST_DIR"

# Create a minimal root module to call the beacon module
mkdir -p "$TEST_DIR/modules/nightly-temporal-anomaly-beacon"
cp src/*.tf "$TEST_DIR/modules/nightly-temporal-anomaly-beacon/"

cat <<EOF > "$TEST_DIR/main.tf"
provider "aws" {
  region = "us-east-1" # Mock region for validation
  # No actual credentials needed for 'terraform validate'
}

module "anomaly_beacon_test" {
  source             = "./modules/nightly-temporal-anomaly-beacon"
  bucket_name_prefix = "test-beacon"
  aws_region         = "us-east-1"
  environment        = "test"
}

output "test_bucket_id" {
  value = module.anomaly_beacon_test.bucket_id
}
EOF

echo "Initializing Terraform in $TEST_DIR..."
# Use -backend=false to avoid needing a real state backend for init
terraform -chdir="$TEST_DIR" init -backend=false > /dev/null

echo "Validating Terraform configuration..."
terraform -chdir="$TEST_DIR" validate

if [ $? -eq 0 ]; then
  echo "Terraform validation successful!"
else
  echo "Terraform validation failed!"
  exit 1
fi

echo "Test complete."
