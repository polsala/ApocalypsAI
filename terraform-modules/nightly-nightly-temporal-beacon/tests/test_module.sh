#!/bin/bash
set -e

echo "Running Terraform module tests..."

# Clean up previous runs to ensure a fresh test environment
rm -rf src/.terraform src/.terraform.lock.hcl src/lambda/beacon.zip

cd src

# Mock rationale: `terraform init -backend=false` and `terraform validate`
# are inherently offline and deterministic. They check the module's syntax,
# variable definitions, and resource graph consistency without requiring
# any interaction with cloud providers or external services.
# This ensures the module is syntactically correct and well-formed, which
# is the primary goal of an offline Terraform module test.

echo "Initializing Terraform (backend disabled for offline testing)..."
terraform init -backend=false

echo "Validating Terraform configuration..."
terraform validate

echo "All Terraform module tests passed: configuration is valid."
