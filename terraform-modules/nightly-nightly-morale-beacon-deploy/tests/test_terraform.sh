#!/bin/bash
set -euo pipefail

echo "Running Terraform validation and formatting checks..."

# Change to the src directory to run terraform commands
cd src

# Validate Terraform configuration syntax
echo "--> Running 'terraform validate'..."
terraform validate

# Check Terraform formatting
echo "--> Running 'terraform fmt -check=true'..."
terraform fmt -check=true

echo "Terraform checks passed successfully!"
