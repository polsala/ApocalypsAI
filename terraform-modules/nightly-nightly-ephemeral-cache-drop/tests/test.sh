#!/bin/bash
set -euo pipefail

echo "--- Initializing Terraform in test directory ---"
terraform init -backend=false # -backend=false prevents state backend configuration

echo "--- Validating Terraform configuration ---"
terraform validate

echo "--- Generating Terraform plan (no actual deployment) ---"
# We use -out=tfplan to ensure a plan can be generated successfully.
terraform plan -out=tfplan

echo "--- Cleaning up generated plan file ---"
rm -f tfplan

echo "--- Terraform module tests passed successfully! ---"
