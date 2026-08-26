#!/usr/bin/env bash
# Mock rationale: This script validates the Terraform configuration locally without contacting AWS.
set -e

echo "Initializing Terraform (backend disabled)..."
terraform init -backend=false > /dev/null

echo "Running terraform validate..."
terraform validate

echo "All checks passed."
