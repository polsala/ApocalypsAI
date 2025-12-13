#!/usr/bin/env bash
set -e

# Mock rationale: This test runs terraform validate offline; no real AWS calls are made.

terraform init -backend=false > /dev/null

tf_output=$(terraform validate 2>&1)

echo "Terraform validation output:"
echo "$tf_output"

echo "PASS: Terraform configuration validates"
