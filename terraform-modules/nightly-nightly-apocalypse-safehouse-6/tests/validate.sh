#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Use local backend and disable provider download to keep the test deterministic and offline.
# Initialize Terraform without contacting remote services.
terraform init -backend=false -input=false -get=false > /dev/null 2>&1

# Validate the configuration.
if terraform validate -no-color; then
  echo "✅ Terraform configuration is valid."
  exit 0
else
  echo "❌ Terraform configuration is invalid."
  exit 1
fi
