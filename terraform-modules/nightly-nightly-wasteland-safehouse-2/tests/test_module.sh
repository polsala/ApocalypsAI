#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: This test runs terraform init and validate locally.
# It does not require real AWS credentials because no apply is performed.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODULE_DIR="${SCRIPT_DIR}/.."

cd "${MODULE_DIR}"

# Initialize without backend or plugin download (assumes plugins are cached)
terraform init -backend=false -input=false -get=false > /dev/null

# Validate configuration syntax
terraform validate

echo "✅ Terraform module validation passed"
