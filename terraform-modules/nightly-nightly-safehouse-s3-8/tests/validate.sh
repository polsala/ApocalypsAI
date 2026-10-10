#!/usr/bin/env bash
# Mock rationale: This script runs terraform init and validate to ensure the module syntax is correct.
set -e

# Initialize Terraform without a backend to keep the test offline
terraform init -backend=false > /dev/null

# Validate the configuration
terraform validate

echo "Terraform validation passed."
