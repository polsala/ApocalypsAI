#!/usr/bin/env bash
set -e

# Mock rationale: This test runs the module locally using the null backend,
# applies it with a known set of variables, and verifies that the expected
# files are created. No external services are required.

TEST_DIR=$(mktemp -d)
cp -R . "$TEST_DIR/module"
cd "$TEST_DIR/module"

terraform init -backend=false -input=false > /dev/null

tf_apply_output=$(terraform apply -auto-approve -input=false \
  -var 'safehouse_name=test_hut' \
  -var 'supplies=["water","food","medicine"]' 2>&1)

EXPECTED_DIR="${PWD}/test_hut"
if [ ! -d "$EXPECTED_DIR" ]; then
  echo "FAIL: safehouse directory not created"
  exit 1
fi

for file in water.txt food.txt medicine.txt; do
  if [ ! -f "$EXPECTED_DIR/$file" ]; then
    echo "FAIL: $file not found"
    exit 1
  fi
done

echo "PASS"
# Clean up
rm -rf "$TEST_DIR"
