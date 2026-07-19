#!/usr/bin/env bash
# Test script for nightly-safehouse-s3 Terraform module
set -e

# Ensure terraform is available; if not, skip tests (offline CI may not have it)
if ! command -v terraform >/dev/null 2>&1; then
  echo "Terraform not found, skipping tests."
  exit 0
fi

# Initialise without remote backend to keep everything local
terraform init -backend=false -input=false >/dev/null

# Validate configuration syntax (does not require network for providers)
terraform validate -no-color

# Basic sanity checks – ensure expected resources are declared
grep -q 'resource "aws_s3_bucket" "safehouse"' main.tf
grep -q 'resource "aws_s3_bucket_object" "supply_cache"' main.tf

echo "All checks passed."
