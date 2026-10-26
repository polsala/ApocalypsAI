#!/usr/bin/env bash
set -e

# Mock rationale: Use local backend and a stubbed AWS provider to avoid real network calls.
# Initialise Terraform without a remote backend.
terraform init -backend=false > /dev/null 2>&1

# Validate the configuration syntax.
terraform validate

# Generate a plan (no‑op, no actual AWS interaction).
PLAN_OUTPUT=$(terraform plan -no-color -input=false 2>&1 || true)

# Ensure versioning is enabled.
if ! echo "$PLAN_OUTPUT" | grep -q "versioning.*enabled = true"; then
  echo "❌ Versioning not enabled"
  exit 1
fi

# Ensure server‑side encryption is set to AES256.
if ! echo "$PLAN_OUTPUT" | grep -q "sse_algorithm = \"AES256\""; then
  echo "❌ SSE algorithm not set to AES256"
  exit 1
fi

# Ensure lifecycle rule expires objects after 30 days.
if ! echo "$PLAN_OUTPUT" | grep -q "expiration.*days = 30"; then
  echo "❌ Lifecycle expiration not set to 30 days"
  exit 1
fi

echo "✅ All checks passed."
