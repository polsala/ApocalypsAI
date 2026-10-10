#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Ensure Terraform configuration validates and plans without real AWS credentials.
# Initialize Terraform with a local (no‑backend) configuration.
terraform init -backend=false -input=false > /dev/null

# Validate the configuration syntax.
terraform validate

# Run a dry‑run plan using a unique bucket name to avoid name collisions.
terraform plan -input=false -var="bucket_name=test-bucket-$(date +%s)" -out=plan.out > /dev/null

echo "All Terraform checks passed."
