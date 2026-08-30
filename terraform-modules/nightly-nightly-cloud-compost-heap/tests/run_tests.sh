#!/bin/bash

set -euo pipefail

echo "Running Terraform validation tests..."

# Initialize Terraform in the test directory
# -backend=false ensures no state backend is configured, keeping it offline.
# -input=false prevents interactive prompts.
terraform -chdir=tests init -backend=false -input=false

# Validate the module configuration
# This checks HCL syntax and variable definitions without needing AWS credentials.
terraform -chdir=tests validate

if [ $? -eq 0 ]; then
  echo "Terraform validation successful!"
else
  echo "Terraform validation failed!"
  exit 1
fi

# Test with a plan to ensure no obvious errors in resource definitions,
# but without applying or requiring live credentials for this structural check.
# -destroy generates a plan to destroy all resources, which is a good way to
# check the HCL without creating actual resources.
# -out=/dev/null discards the plan file.
# Mock rationale: 'terraform plan' can be run without actual credentials
# if the provider is configured with dummy values (as in tests/main.tf)
# or if it's a local module. This is a structural check, not a live resource check.
terraform -chdir=tests plan -destroy -out=/dev/null -input=false

if [ $? -eq 0 ]; then
  echo "Terraform plan (destroy) successful!"
else
  echo "Terraform plan (destroy) failed!"
  exit 1
fi

echo "All tests passed!"
