#!/bin/bash
set -euo pipefail

echo "--- Running Terraform Plan Test for Nightly Temporal Outpost Provisioner ---"

# Navigate to the src directory
cd src

# Initialize Terraform in a clean, non-backend mode for testing
# This prevents state files from being created and doesn't require actual cloud credentials.
# Mock rationale: 'terraform init -backend=false' allows local validation of provider
# and module syntax without connecting to a remote backend or requiring real credentials.
# It effectively "mocks" the backend setup.
echo "Initializing Terraform..."
terraform init -backend=false > /dev/null

# Run terraform plan and capture output
# Use specific test variables to ensure deterministic output.
# -no-color for easier parsing.
# Mock rationale: 'terraform plan' itself is a dry-run. By providing dummy but valid-looking
# AMI and instance_type, we can validate the configuration's structure and expected changes
# without making actual AWS API calls. The AWS provider is implicitly "mocked" in this dry-run context.
echo "Running terraform plan..."
PLAN_OUTPUT=$(terraform plan -no-color \
  -var="region=us-east-1" \
  -var="instance_type=t2.micro" \
  -var="ami=ami-test-1234567890abcdef0" \
  -var="outpost_name=test-temporal-outpost" \
  -var="self_destruct_after_minutes=1" \
  -input=false)

# Check for expected resources in the plan output
echo "Verifying plan output..."

if echo "${PLAN_OUTPUT}" | grep -q "aws_instance.outpost"; then
  echo "PASS: aws_instance.outpost found in plan."
else
  echo "FAIL: aws_instance.outpost NOT found in plan."
  echo "${PLAN_OUTPUT}"
  exit 1
fi

if echo "${PLAN_OUTPUT}" | grep -q "aws_security_group.outpost_sg"; then
  echo "PASS: aws_security_group.outpost_sg found in plan."
else
  echo "FAIL: aws_security_group.outpost_sg NOT found in plan."
  echo "${PLAN_OUTPUT}"
  exit 1
fi

# Check for expected output values (these appear in the plan if they are known after apply)
# For outputs that depend on resource IDs (like public_ip, instance_id), they will show as "(known after apply)"
# but the 'destroy_command' and 'self_destruct_reminder' should be fully formed.
if echo "${PLAN_OUTPUT}" | grep -q "destroy_command = \"To initiate the temporal outpost's self-destruct sequence, run: terraform destroy -auto-approve\""; then
  echo "PASS: Expected destroy_command output found in plan."
else
  echo "FAIL: Expected destroy_command output NOT found in plan."
  echo "${PLAN_OUTPUT}"
  exit 1
fi

if echo "${PLAN_OUTPUT}" | grep -q "self_destruct_reminder = \"This temporal outpost is intended to exist for approximately 1 minutes. Please remember to run 'terraform destroy' when your mission is complete.\""; then
  echo "PASS: Expected self_destruct_reminder output found in plan."
else
  echo "FAIL: Expected self_destruct_reminder output NOT found in plan."
  echo "${PLAN_OUTPUT}"
  exit 1
fi

echo "--- All Terraform Plan Tests Passed! ---"
