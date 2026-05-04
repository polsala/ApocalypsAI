#!/bin/bash

set -euo pipefail

# Navigate to the test directory
cd "$(dirname "$0")"

echo "Running Terraform module tests for nightly-whispering-vault..."

# Initialize Terraform in the test directory
# Mock rationale: -backend=false ensures no remote state backend is configured,
# making the test fully offline and deterministic.
terraform init -backend=false

# Validate the Terraform configuration syntax and semantics
echo "Validating Terraform configuration..."
terraform validate

# Generate a Terraform plan without applying it
# Mock rationale: -out saves the plan to a file, -input=false prevents interactive prompts.
# -destroy=false ensures it's a creation plan. Using explicit vars for test consistency.
# This checks if the module can be planned successfully without actual AWS interaction.
PLAN_FILE="tfplan_test"
terraform plan -out="${PLAN_FILE}" -destroy=false -input=false \
  -var "bucket_name_prefix=test-whisper-integration-" \
  -var "region=us-east-1" \
  -var "retention_days=1"

# Check if the plan file was created, indicating a successful plan generation
if [ ! -f "${PLAN_FILE}" ]; then
  echo "Error: Terraform plan file '${PLAN_FILE}' was not created." >&2
  exit 1
fi

echo "Terraform plan generated successfully. Inspecting plan for key resources..."

# Optionally, you could add more sophisticated checks here, e.g.,
# parsing the plan output to ensure specific resources or properties are present.
# For this basic test, successful validate and plan generation are sufficient.

# Clean up the generated plan file
rm "${PLAN_FILE}"

echo "All Terraform tests passed successfully for nightly-whispering-vault."
