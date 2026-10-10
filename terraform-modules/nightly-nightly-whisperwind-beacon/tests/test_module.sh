#!/bin/bash
set -euo pipefail

echo "Running Terraform module validation tests..."

# Mock rationale: terraform validate performs static analysis of HCL syntax
# and configuration without requiring network access or cloud provider credentials.
# It's deterministic and offline, checking for syntactical correctness and
# basic logical consistency within the module.

# Validate the module's source code
echo "Validating src/ directory..."
terraform validate src/

# Check formatting
echo "Checking Terraform formatting in src/..."
terraform fmt --check src/

echo "All Terraform module validation tests passed."
