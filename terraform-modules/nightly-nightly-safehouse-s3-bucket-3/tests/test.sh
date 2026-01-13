#!/usr/bin/env bash
set -e

# Initialise Terraform without a remote backend (offline safe)
terraform init -backend=false > /dev/null

# Validate the configuration syntax
terraform validate

# Basic sanity checks on the generated HCL
if ! grep -q 'resource "aws_s3_bucket"' main.tf; then
  echo "Bucket resource missing"
  exit 1
fi

if ! grep -q 'versioning {' main.tf; then
  echo "Versioning block missing"
  exit 1
fi

if ! grep -q 'lifecycle_rule {' main.tf; then
  echo "Lifecycle rule block missing"
  exit 1
fi

echo "All checks passed"

