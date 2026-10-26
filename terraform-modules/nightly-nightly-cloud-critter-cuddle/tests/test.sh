#!/bin/bash

# Mock rationale: This script performs a dry run using 'terraform plan'
# to validate the module's syntax and variable usage. It does not
# provision any actual cloud resources, making it deterministic and offline.
# It checks if Terraform can initialize the providers and generate a plan
# successfully with the provided mock configuration.

set -euo pipefail

echo "--- Running Terraform module tests ---"

# Navigate to the tests directory
cd "$(dirname "$0")"

# Initialize Terraform (downloads providers, validates configuration)
echo "Initializing Terraform..."
terraform init -backend=false # -backend=false prevents state backend configuration

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate

# Generate a plan (dry run)
echo "Generating Terraform plan (dry run)..."
terraform plan -out=tfplan -input=false -no-color

# Check if the plan file was created, indicating success
if [ -f tfplan ]; then
  echo "Terraform plan generated successfully. Test passed."
  rm tfplan # Clean up the plan file
  exit 0
else
  echo "Terraform plan failed to generate. Test failed."
  exit 1
fi
