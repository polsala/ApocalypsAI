#!/bin/bash
set -euo pipefail

echo "--- Running Terraform module tests ---"

# Define test variables
TEST_CONSTELLATION_NAME="Ursa Major"
TEST_ENVIRONMENT="staging"
TEST_ADDITIONAL_TAGS='{"Project":"Stargazer","CostCenter":"Alpha"}'

# Initialize Terraform in the test directory
echo "Initializing Terraform..."
terraform -chdir=./ init -backend=false > /dev/null

# Plan and capture output as JSON
echo "Planning Terraform configuration..."
PLAN_OUTPUT=$(terraform -chdir=./ plan -var="test_constellation_name=${TEST_CONSTELLATION_NAME}" \
                                      -var="test_environment=${TEST_ENVIRONMENT}" \
                                      -var="test_additional_tags=${TEST_ADDITIONAL_TAGS}" \
                                      -json -out=tfplan.json)

# Show the plan in JSON format to extract outputs
echo "Showing Terraform plan JSON..."
SHOW_OUTPUT=$(terraform -chdir=./ show -json tfplan.json)

# Extract planned outputs using jq
PLANNED_PREFIX=$(echo "${SHOW_OUTPUT}" | jq -r '.planned_values.outputs.test_prefix.value')
PLANNED_TAGS=$(echo "${SHOW_OUTPUT}" | jq -r '.planned_values.outputs.test_tags.value')

echo "Planned Prefix: ${PLANNED_PREFIX}"
echo "Planned Tags: ${PLANNED_TAGS}"

# Assertions
echo "--- Running Assertions ---"

# Assert prefix
EXPECTED_PREFIX="ursa-major-staging"
if [[ "${PLANNED_PREFIX}" == "${EXPECTED_PREFIX}" ]]; then
  echo "✅ Prefix assertion passed: '${PLANNED_PREFIX}' matches '${EXPECTED_PREFIX}'"
else
  echo "❌ Prefix assertion failed: Expected '${EXPECTED_PREFIX}', got '${PLANNED_PREFIX}'"
  exit 1
fi

# Assert tags (this is more complex due to JSON string comparison, let's check key-values)
# Expected tags: Constellation, Environment, ManagedBy, Project, CostCenter
if echo "${PLANNED_TAGS}" | jq -e '.Constellation == "Ursa Major"' > /dev/null; then
  echo "✅ Tag 'Constellation' assertion passed."
else
  echo "❌ Tag 'Constellation' assertion failed."
  exit 1
fi

if echo "${PLANNED_TAGS}" | jq -e '.Environment == "staging"' > /dev/null; then
  echo "✅ Tag 'Environment' assertion passed."
else
  echo "❌ Tag 'Environment' assertion failed."
  exit 1
fi

if echo "${PLANNED_TAGS}" | jq -e '.ManagedBy == "ApocalypsAI-ConstellationMapper"' > /dev/null; then
  echo "✅ Tag 'ManagedBy' assertion passed."
else
  echo "❌ Tag 'ManagedBy' assertion failed."
  exit 1
fi

if echo "${PLANNED_TAGS}" | jq -e '.Project == "Stargazer"' > /dev/null; then
  echo "✅ Tag 'Project' assertion passed."
else
  echo "❌ Tag 'Project' assertion failed."
  exit 1
fi

if echo "${PLANNED_TAGS}" | jq -e '.CostCenter == "Alpha"' > /dev/null; then
  echo "✅ Tag 'CostCenter' assertion passed."
else
  echo "❌ Tag 'CostCenter' assertion failed."
  exit 1
fi

echo "--- All tests passed! ---"
rm -f tfplan.json .terraform.lock.hcl
rm -rf .terraform
