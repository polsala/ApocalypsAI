#!/usr/bin/env bash
set -euo pipefail

# Initialize a temporary directory for the test
TEST_DIR=$(mktemp -d)
cleanup() {
  rm -rf "$TEST_DIR"
}
trap cleanup EXIT

# Copy module files into the temp dir
cp -r . "$TEST_DIR/module"

cd "$TEST_DIR/module"

# Initialize Terraform (no backend) – only the random provider is needed
terraform init -backend=false > /dev/null

# Validate the configuration syntax
terraform validate

# Run a plan (no actual resources are created, random_pet is local)
terraform plan -input=false -no-color -out=plan.out > /dev/null

# Apply only the first random_pet to force generation without persisting state
terraform apply -auto-approve -input=false -refresh=false -target=random_pet.apoc_name[0] > /dev/null

# Capture the output as JSON
terraform output -json names > names.json

# Verify that the number of generated names matches the default count (3)
EXPECTED_COUNT=3
ACTUAL_COUNT=$(jq '. | length' names.json)
if [ "$ACTUAL_COUNT" -eq "$EXPECTED_COUNT" ]; then
  echo "Test passed: generated $ACTUAL_COUNT names."
  exit 0
else
  echo "Test failed: expected $EXPECTED_COUNT names, got $ACTUAL_COUNT."
  exit 1
fi
