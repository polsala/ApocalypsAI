#!/usr/bin/env bash
set -e
# Mock rationale: using local backend to avoid remote state; this test validates the module syntax.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."
terraform init -backend=false > /dev/null
terraform validate
echo "Terraform validation succeeded."
