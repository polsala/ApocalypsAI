#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: This test runs terraform commands in a temporary directory
# without contacting AWS, using -backend=false and no provider credentials.
# It validates syntax and ensures the plan can be generated.

TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

cp -R . "$TMPDIR/module"
cd "$TMPDIR/module"

tf init -backend=false > /dev/null
terraform validate

tf plan -input=false -var 'bucket_name=test-safehouse-bucket' -out=plan.out > /dev/null

echo "Terraform module test passed."
