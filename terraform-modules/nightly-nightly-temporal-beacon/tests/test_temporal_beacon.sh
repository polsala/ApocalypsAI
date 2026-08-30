#!/bin/bash
set -euo pipefail

echo "--- Running Terraform Temporal Beacon tests ---"

# Mock rationale: Terraform plan is run without applying,
# so no actual AWS resources are created or modified.
# The AWS provider block in tests/main.tf uses dummy credentials
# which are sufficient for `terraform plan` to generate an output
# without requiring real authentication.

# Initialize Terraform
echo "Initializing Terraform..."
terraform -chdir=./ init -backend=false > /dev/null

# Run terraform plan and capture output
echo "Running terraform plan..."
PLAN_OUTPUT=$(terraform -chdir=./ plan -no-color -out=tfplan)

# Verify that the plan output contains expected resources and tags
echo "Verifying plan output..."

# Check for instance creation
if ! echo "${PLAN_OUTPUT}" | grep -q 'resource "aws_instance" "temporal_beacon"'; then
  echo "Test Failed: Expected 'aws_instance' resource not found in plan."
  exit 1
fi

# Check for instance type
if ! echo "${PLAN_OUTPUT}" | grep -q 'instance_type = "t2.nano"'; then
  echo "Test Failed: Expected instance_type 't2.nano' not found in plan."
  exit 1
fi

# Check for beacon name tag
if ! echo "${PLAN_OUTPUT}" | grep -q 'Name = "TestTemporalAnchor"'; then
  echo "Test Failed: Expected Name tag 'TestTemporalAnchor' not found in plan."
  exit 1
fi

# Check for chronal anchor tag
if ! echo "${PLAN_OUTPUT}" | grep -q 'ChronalAnchor = "TestTimelineStabilizer"'; then
  echo "Test Failed: Expected ChronalAnchor tag 'TestTimelineStabilizer' not found in plan."
  exit 1
fi

# Check for ManagedBy tag
if ! echo "${PLAN_OUTPUT}" | grep -q 'ManagedBy = "ApocalypsAI-NightlyIntegrator"'; then
  echo "Test Failed: Expected ManagedBy tag 'ApocalypsAI-NightlyIntegrator' not found in plan."
  exit 1
fi

echo "All Terraform plan checks passed successfully!"

# Clean up generated plan file
rm tfplan

echo "--- Terraform Temporal Beacon tests completed ---"
