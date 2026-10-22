#!/bin/bash
set -euo pipefail

echo "--- Running Terraform module tests ---"

# Change to the tests directory
cd "$(dirname "$0")"

# Clean up previous runs
rm -rf .terraform .terraform.lock.hcl terraform.tfstate* .terraform.tfstate.lock.info

echo "Initializing Terraform..."
# Mock rationale: terraform init downloads providers. We use a mock provider config
# in main.tf to ensure this step is deterministic and doesn't require actual AWS access.
terraform init -backend=false -input=false

echo "Validating Terraform configuration..."
# Mock rationale: terraform validate checks syntax and configuration logic offline.
terraform validate

echo "Generating Terraform plan and checking for changes..."
# Mock rationale: terraform plan -detailed-exitcode generates an execution plan
# and returns a specific exit code:
# 0 = Succeeded with no changes
# 1 = Error
# 2 = Succeeded with changes
# For a new module, we expect changes (exit code 2) as it defines new resources.
terraform plan -detailed-exitcode -out=tfplan.binary -input=false

PLAN_EXIT_CODE=$?

if [ "$PLAN_EXIT_CODE" -eq 2 ]; then
  echo "Terraform plan indicates resources will be created (expected for initial plan)."
  echo "Verifying plan output for key resources..."
  # Mock rationale: terraform show -json allows inspecting the plan's content offline.
  # We check for the presence of the S3 bucket and its properties.
  PLAN_JSON=$(terraform show -json tfplan.binary)

  if echo "$PLAN_JSON" | grep -q "aws_s3_bucket.wasteland_vault"; then
    echo "  - aws_s3_bucket.wasteland_vault found in plan."
  else
    echo "Error: aws_s3_bucket.wasteland_vault not found in plan."
    exit 1
  fi

  if echo "$PLAN_JSON" | grep -q '"sse_algorithm": "AES256"'; then
    echo "  - SSE-S3 encryption (AES256) found in plan."
  else
    echo "Error: SSE-S3 encryption (AES256) not found in plan."
    exit 1
  fi

  if echo "$PLAN_JSON" | grep -q '"block_public_acls": true'; then
    echo "  - Public access block (block_public_acls) found in plan."
  else
    echo "Error: Public access block (block_public_acls) not found in plan."
    exit 1
  fi

  echo "All checks passed."
  exit 0
elif [ "$PLAN_EXIT_CODE" -eq 0 ]; then
  echo "Terraform plan indicates no changes (unexpected for initial plan, but might happen if state exists)."
  echo "This test expects new resources to be planned (exit code 2)."
  exit 1
else
  echo "Terraform plan failed with exit code $PLAN_EXIT_CODE."
  exit 1
fi
