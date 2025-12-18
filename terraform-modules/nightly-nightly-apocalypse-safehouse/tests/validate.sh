#!/usr/bin/env bash
# Mock rationale: Validate that the module files contain expected resource blocks.

set -e

# Check main.tf contains random_pet
if ! grep -q 'resource "random_pet" "name"' main.tf; then
  echo "Missing random_pet resource"
  exit 1
fi

# Check main.tf contains random_id
if ! grep -q 'resource "random_id" "id"' main.tf; then
  echo "Missing random_id resource"
  exit 1
fi

# Check main.tf contains null_resource radiation_shield
if ! grep -q 'resource "null_resource" "radiation_shield"' main.tf; then
  echo "Missing null_resource radiation_shield"
  exit 1
fi

echo "All checks passed."
