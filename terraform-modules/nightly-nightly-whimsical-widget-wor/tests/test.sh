#!/bin/bash

set -euo pipefail

echo "Running Terraform module tests..."

# Initialize Terraform in the test directory
# -backend=false prevents Terraform from trying to configure a state backend,
# which is not needed for syntax validation and plan generation.
terraform init -backend=false

# Validate the Terraform configuration syntax
echo "Validating Terraform configuration..."
terraform validate

if [ $? -ne 0 ]; then
  echo "Terraform validation failed!"
  exit 1
fi

# Generate a Terraform plan to ensure resources can be defined
# -out=tfplan creates a plan file, -no-color removes ANSI escape codes for easier parsing (though not strictly needed here)
echo "Generating Terraform plan..."
terraform plan -out=tfplan -no-color

if [ $? -ne 0 ]; then
  echo "Terraform plan generation failed!"
  exit 1
fi

# Clean up the generated plan file
rm tfplan

echo "Terraform module tests passed successfully!"
exit 0
