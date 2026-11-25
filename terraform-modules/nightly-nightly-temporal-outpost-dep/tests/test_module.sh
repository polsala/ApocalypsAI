#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests..."

# Create a temporary directory for testing
TEST_DIR=$(mktemp -d)
echo "Temporary test directory: $TEST_DIR"
cd "$TEST_DIR"

# Copy module source into a subdirectory
mkdir -p module_under_test
cp -r ../src/* module_under_test/

# Create a minimal root configuration to call the module
cat <<EOF > main.tf
provider "aws" {
  region = "us-east-1" # Mock rationale: Use a default region for validation/plan, no actual deployment.
}

module "temporal_outpost" {
  source = "./module_under_test"
  name_prefix = "test-apocalypsai-outpost"
  bucket_name = "test-apocalypsai-temporal-logs-$(date +%s)" # Mock rationale: Unique bucket name for plan validation, avoiding actual S3 uniqueness constraints.
  schedule_expression = "rate(1 minute)" # Mock rationale: A valid schedule expression for plan validation.
}
EOF

echo "Initializing Terraform..."
# Mock rationale: For offline testing, assume providers are already downloaded or available in the Terraform cache.
# In a real CI environment, this step might require network access for the first run to download providers.
# We use -backend=false to avoid state file issues in a temporary directory.
terraform init -backend=false

if [ $? -ne 0 ]; then
  echo "Terraform initialization failed!"
  exit 1
fi

echo "Validating Terraform configuration..."
terraform validate

if [ $? -ne 0 ]; then
  echo "Terraform validation failed!"
  exit 1
fi
echo "Terraform validation passed."

echo "Generating Terraform plan..."
# -input=false prevents interactive prompts
# -no-color removes ANSI escape codes from output, making it easier to parse if needed
terraform plan -out=tfplan -input=false -no-color

if [ $? -ne 0 ]; then
  echo "Terraform plan generation failed!"
  exit 1
fi
echo "Terraform plan generated successfully."

# Optional: Further checks on the plan output (e.g., resource counts, specific properties)
# For this exercise, ensuring plan generation without errors is sufficient for "offline" testing.
# Example of checking plan output:
# if ! terraform show -json tfplan | grep -q '"type": "aws_lambda_function"'; then
#   echo "Error: aws_lambda_function resource not found in plan!"
#   exit 1
# fi

echo "All Terraform module tests passed!"

# Clean up temporary directory
cd - > /dev/null
rm -rf "$TEST_DIR"
