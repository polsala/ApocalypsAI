#!/usr/bin/env bash
set -e

# Initialize Terraform without downloading providers (mocked)
terraform init -backend=false -get=false > /dev/null 2>&1 || {
  echo "Terraform init failed (mocked environment)."
  exit 1
}

# Validate configuration (mocked)
terraform validate -no-color > /dev/null 2>&1 || {
  echo "Terraform validate failed (mocked environment)."
  exit 1
}

# Mock plan execution (no actual AWS interaction)
echo "Mock plan succeeded."
exit 0
# Mock rationale: The test runs terraform commands with -get=false to avoid network calls.
# In a real CI environment, providers would be cached, making this deterministic.
