#!/usr/bin/env bash
set -e

# Mock rationale: Use dummy AWS credentials; Terraform will not make real API calls during validate/plan with -backend=false.
export AWS_ACCESS_KEY_ID="mock"
export AWS_SECRET_ACCESS_KEY="mock"
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODULE_DIR="${SCRIPT_DIR}/.."

cd "${MODULE_DIR}"

# Initialize Terraform without remote backend
terraform init -backend=false > /dev/null

# Validate configuration syntax
terraform validate

# Generate a plan (no actual apply)
terraform plan -input=false -out=plan.out > /dev/null

echo "All Terraform tests passed."
