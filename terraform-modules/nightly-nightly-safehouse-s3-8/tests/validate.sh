#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: This script runs terraform init (local backend) and validate.
# It does not contact AWS because no provider configuration is supplied.
# The test passes if terraform validate succeeds.

tf_init_output=$(terraform init -backend=false 2>&1) || {
  echo "Terraform init failed:" >&2
  echo "$tf_init_output" >&2
  exit 1
}

tf_validate_output=$(terraform validate 2>&1) || {
  echo "Terraform validate failed:" >&2
  echo "$tf_validate_output" >&2
  exit 1
}

echo "Terraform module validation passed."
