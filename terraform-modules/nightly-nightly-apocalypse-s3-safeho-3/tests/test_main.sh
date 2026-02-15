#!/usr/bin/env bash
set -e

# Initialize Terraform with no backend (local)
terraform -chdir=../src init -backend=false > /dev/null

# Validate configuration (syntax only, no provider calls)
terraform -chdir=../src validate

echo "All Terraform checks passed."
# Mock rationale: This test runs entirely offline; it only checks that the HCL syntax is valid and that required providers are declared.
