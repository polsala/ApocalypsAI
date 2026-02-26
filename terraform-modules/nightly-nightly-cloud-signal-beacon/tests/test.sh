#!/bin/bash
set -euo pipefail

echo "Running Terraform module validation tests..."

# Change to the tests directory
cd "$(dirname "$0")"

# Initialize Terraform in the tests directory
# Mock rationale: This initializes the module for validation without needing AWS credentials
# or actually downloading provider plugins, making it deterministic and offline.
# -backend=false: Prevents Terraform from configuring a state backend.
# -get-plugins=false: Prevents Terraform from downloading provider plugins.
terraform init -backend=false -get-plugins=false

# Validate the Terraform configuration
# Mock rationale: This checks for syntax errors, variable definitions, and configuration issues
# within the module and its usage, without interacting with a real cloud provider.
terraform validate

echo "Terraform module validation successful!"
