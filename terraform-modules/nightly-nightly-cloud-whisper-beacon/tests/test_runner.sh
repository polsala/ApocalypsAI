#!/bin/bash
set -euo pipefail

echo "Running Terraform validation tests..."

# Initialize Terraform in the test directory
# -backend=false prevents Terraform from trying to configure a backend,
# making the test truly offline and self-contained.
terraform -chdir=tests init -backend=false

# Validate the Terraform configuration
# This checks syntax, variable definitions, and module references.
terraform -chdir=tests validate

echo "Terraform validation successful!"

# Clean up generated files
rm -rf tests/.terraform tests/.terraform.lock.hcl || true

echo "All tests passed for nightly-cloud-whisper-beacon."
