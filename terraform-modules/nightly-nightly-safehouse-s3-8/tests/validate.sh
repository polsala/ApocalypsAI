#!/usr/bin/env bash
set -e

# Mock rationale: This script runs terraform init and validate in a deterministic offline manner.
# No actual AWS calls are made because the backend is disabled and no provider configuration is required
# for validation.

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
