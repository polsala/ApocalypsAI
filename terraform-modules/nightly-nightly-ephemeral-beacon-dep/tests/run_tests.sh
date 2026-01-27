#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests..."

TEST_DIR="tests"
FIXTURE_DIR="." # test_beacon_deployment.tf is directly in tests/

# Clean up any previous Terraform state or cache
rm -rf "${FIXTURE_DIR}/.terraform" "${FIXTURE_DIR}/.terraform.lock.hcl" "${FIXTURE_DIR}/terraform.tfstate*"

echo "Initializing Terraform in ${FIXTURE_DIR}..."
terraform -chdir="${FIXTURE_DIR}" init -backend=false # Mock rationale: -backend=false prevents state storage, keeping it offline.

echo "Validating Terraform configuration in ${FIXTURE_DIR}..."
terraform -chdir="${FIXTURE_DIR}" validate # Mock rationale: Validates syntax and configuration without cloud interaction.

echo "Generating Terraform plan for ${FIXTURE_DIR} (no apply)..."
# terraform plan will fail if there are issues, and it shows what *would* be created.
# We don't need to parse the output for this simple test, just ensure it runs without error.
terraform -chdir="${FIXTURE_DIR}" plan -out="${FIXTURE_DIR}/test.tfplan" -input=false # Mock rationale: Generates a plan file offline, simulating a deployment preview.

echo "Tests passed successfully!"

# Clean up generated plan file
rm -f "${FIXTURE_DIR}/test.tfplan"
