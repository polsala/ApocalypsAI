#!/usr/bin/env bash
set -e

# Initialize Terraform with a local (no‑backend) configuration
terraform init -backend=false > /dev/null

# Validate the configuration – should succeed with the mock AWS provider
terraform validate

echo "✅ Terraform configuration is valid."
