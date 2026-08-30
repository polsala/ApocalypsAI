#!/usr/bin/env bash
# test_module.sh – deterministic offline test for nightly‑safehouse‑s3
# Mock rationale: we avoid real AWS calls; we only verify that the generated
# Terraform files contain the expected resource blocks and variables.

set -euo pipefail

MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 1. Ensure required files exist
for f in main.tf variables.tf outputs.tf; do
  if [[ ! -f "${MODULE_DIR}/src/${f}" ]]; then
    echo "Missing ${f} in src/"
    exit 1
  fi
done

# 2. Simple content checks
if ! grep -q "resource \"aws_s3_bucket\" \"safehouse\"" "${MODULE_DIR}/src/main.tf"; then
  echo "aws_s3_bucket \"safehouse\" not defined"
  exit 1
fi

if ! grep -q "variable \"bucket_name_prefix\"" "${MODULE_DIR}/src/variables.tf"; then
  echo "bucket_name_prefix variable missing"
  exit 1
fi

if ! grep -q "output \"supply_url\"" "${MODULE_DIR}/src/outputs.tf"; then
  echo "supply_url output missing"
  exit 1
fi

# 3. Run terraform validate (offline – no provider download)
pushd "${MODULE_DIR}/src" > /dev/null
terraform init -backend=false -get=false > /dev/null 2>&1 || true
# The init may attempt to download the AWS provider; we suppress errors because we are offline.
# Validate will succeed as long as the syntax is correct.
terraform validate -no-color || {
  echo "terraform validate failed"
  exit 1
}
popd > /dev/null

echo "All checks passed."
