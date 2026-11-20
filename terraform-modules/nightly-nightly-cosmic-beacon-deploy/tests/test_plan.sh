#!/bin/bash
set -euo pipefail

# Mock rationale: This test runs `terraform validate` and `terraform plan`
# to ensure the module's syntax is correct and a deployment plan can be generated.
# It does not interact with actual AWS APIs, making it deterministic and offline.
# The `terraform init -backend=false` command prevents Terraform from trying to
# configure a state backend, which would require network access.
# The `terraform plan -out=tfplan` command generates a plan file without applying it.

echo "--- Running Terraform module tests ---"

# Create a temporary directory for the test environment
TEST_DIR=$(mktemp -d)
echo "Temporary test directory: $TEST_DIR"
cp -r src "$TEST_DIR/"
cd "$TEST_DIR"

# Create a minimal root module to call the beacon module
cat <<EOF > main.tf
module "cosmic_beacon_test" {
  source = "./src"
  aws_region = "us-east-1" # Mock region for plan generation
  instance_type = "t3.nano" # Use a small instance type for testing
  min_size = 1
  max_size = 1
  desired_capacity = 1
  ami_id = "ami-053b0d534c2791404" # Mock AMI for plan generation (Amazon Linux 2023 us-east-1)
}
EOF

echo "1. Initializing Terraform..."
terraform init -backend=false # Mock rationale: Prevents network calls for state backend config.
if [ $? -ne 0 ]; then
    echo "Terraform init failed!"
    exit 1
fi
echo "Terraform init successful."

echo "2. Validating Terraform configuration..."
terraform validate
if [ $? -ne 0 ]; then
    echo "Terraform validation failed!"
    exit 1
fi
echo "Terraform validation successful."

echo "3. Generating Terraform plan..."
# -detailed-exitcode: 0=no changes, 1=error, 2=changes
# We expect changes because we're planning to create resources.
terraform plan -out=tfplan -detailed-exitcode
PLAN_EXIT_CODE=$?

if [ $PLAN_EXIT_CODE -eq 1 ]; then
    echo "Terraform plan failed with an error!"
    exit 1
elif [ $PLAN_EXIT_CODE -eq 0 ]; then
    echo "Terraform plan showed no changes, which is unexpected for a new deployment."
    echo "This might indicate an issue or that resources are already defined."
    exit 1 # Fail if no changes are planned for a new module
fi

echo "Terraform plan generated successfully (exit code: $PLAN_EXIT_CODE, expected 2 for changes)."

# Optional: Further checks on the plan file (e.g., using `terraform show -json tfplan`)
# For this utility, basic plan generation is sufficient.

echo "--- All Terraform module tests passed! ---"

# Clean up temporary directory
cd - > /dev/null
rm -rf "$TEST_DIR"
