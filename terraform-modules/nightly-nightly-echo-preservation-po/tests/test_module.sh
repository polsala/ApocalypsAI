#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests..."

# Navigate to the test fixture directory
cd "$(dirname "$0")"

# Mock rationale: terraform init downloads providers but does not interact with cloud APIs.
# It's a prerequisite for validate and plan. We disable the backend to ensure no remote state interaction.
echo "Initializing Terraform..."
terraform init -backend=false
if [ $? -ne 0 ]; then
  echo "Terraform init failed!"
  exit 1
fi

# Mock rationale: terraform validate checks syntax and configuration validity offline.
# It does not require cloud credentials or interact with cloud APIs.
echo "Validating Terraform configuration..."
terraform validate
if [ $? -ne 0 ]; then
  echo "Terraform validation failed!"
  exit 1
fi

# Mock rationale: terraform fmt --check ensures consistent code formatting offline.
echo "Checking Terraform formatting..."
terraform fmt --check
if [ $? -ne 0 ]; then
  echo "Terraform formatting check failed! Run 'terraform fmt' to fix."
  exit 1
fi

# Mock rationale: terraform plan can be used to generate an execution plan.
# For a truly offline and deterministic test, we primarily rely on `validate` and `fmt`.
# A full `plan` or `apply` for AWS resources would require AWS credentials and thus not be offline.
# We skip the `plan` step to ensure the test remains fully offline as per requirements.

echo "All offline Terraform module tests passed successfully!"
