#!/usr/bin/env bash
set -e

# Mock rationale: offline test, no real AWS credentials needed.
# Initialize the module without a backend and validate syntax.

cd "$(dirname "$0")/.."

tf init -backend=false > /dev/null 2>&1

tf validate

echo "✅ Terraform module validation passed."
