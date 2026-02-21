#!/bin/bash

set -euo pipefail

# Mock rationale: This test script performs offline validation and plan generation.
# It does not provision actual cloud resources. It checks the module's syntax,
# variable validation, and ensures a plan can be successfully generated.
# The AWS provider initialization for `terraform init` and `terraform plan`
# is assumed to be configured minimally (e.g., via environment variables or ~/.aws/credentials)
# but no live API calls are strictly necessary for the *module's* internal consistency checks.
# The 'plan' step will simulate what *would* happen without making actual changes.

echo "Running Terraform module tests..."

# Navigate to the test configuration directory
cd "$(dirname "$0")"

# Initialize Terraform (download providers, but no backend config)
# -backend=false prevents Terraform from trying to configure a state backend, making it more offline.
echo "Initializing Terraform..."
terraform init -backend=false

if [ $? -ne 0 ]; then
  echo "Terraform init failed!" >&2
  exit 1
fi

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

if [ $? -ne 0 ]; then
  echo "Terraform validation failed!" >&2
  exit 1
fi

# Generate a plan without applying it
# -input=false prevents interactive prompts
# -out=tfplan saves the plan to a file for potential inspection (though not strictly checked here)
echo "Generating Terraform plan..."
terraform plan -out=tfplan -input=false

if [ $? -ne 0 ]; then
  echo "Terraform plan generation failed!" >&2
  exit 1
fi

# Clean up the generated plan file
rm tfplan

echo "Terraform module tests passed successfully!"
