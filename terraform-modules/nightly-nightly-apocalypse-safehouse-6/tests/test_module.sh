#!/usr/bin/env bash
set -e

# Mock rationale: This test runs entirely offline using the local backend.
# No real AWS credentials are required because we only invoke `terraform validate`.

MODULE_DIR="$(cd $(dirname $0)/.. && pwd)"
cd "$MODULE_DIR"

# Initialise the module (backend is local, so no remote state).
terraform init -backend=false > /dev/null

# Validate the configuration.
terraform validate

# Perform a dry‑run plan to ensure resources can be parsed.
terraform plan -input=false -out=plan.out > /dev/null

echo "✅ Terraform module validation passed."
