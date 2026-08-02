#!/usr/bin/env bash
set -euo pipefail

# Initialize Terraform (offline, no backend)
terraform -chdir=../src init -backend=false > /dev/null

# Validate configuration
terraform -chdir=../src validate

# Apply with example variables
terraform -chdir=../src apply -auto-approve -input=false \
  -var 'file_path=tmp/testfile' \
  -var 'content=Apocalypse Safehouse' > /dev/null

# Determine expected file path
suffix=$(terraform -chdir=../src output -raw random_suffix)
expected_path="tmp/testfile-${suffix}"

# Verify file exists and contains expected content
if [[ ! -f "$expected_path" ]]; then
  echo "FAIL: Expected file $expected_path does not exist"
  exit 1
fi

content=$(cat "$expected_path")
if [[ "$content" != "Apocalypse Safehouse" ]]; then
  echo "FAIL: File content mismatch"
  exit 1
fi

echo "PASS: Terraform module works as expected"

# Cleanup
rm -f "$expected_path"
terraform -chdir=../src destroy -auto-approve -input=false > /dev/null
