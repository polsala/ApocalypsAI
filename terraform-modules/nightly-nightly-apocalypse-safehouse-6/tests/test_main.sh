#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Use local backend and validate syntax only.
terraform init -backend=false > /dev/null 2>&1
terraform validate > /dev/null 2>&1

echo "Terraform module validation passed."
