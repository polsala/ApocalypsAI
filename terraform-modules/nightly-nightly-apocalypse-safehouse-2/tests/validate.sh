#!/usr/bin/env bash
set -e

# Mock rationale: Using local backend to avoid remote state.
terraform init -backend=false > /dev/null

# Validate syntax
terraform validate

# Generate a plan (no apply)
terraform plan -out=plan.out > /dev/null

echo "Terraform module validation and plan succeeded."
