#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests..."

# Navigate to the test directory
cd "$(dirname "$0")"

# Initialize Terraform (backend=false for offline testing)
echo "Initializing Terraform..."
terraform init -backend=false -input=false > /dev/null
if [ $? -ne 0 ]; then
  echo "Terraform init failed!"
  exit 1
fi
echo "Terraform init successful."

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate > /dev/null
if [ $? -ne 0 ]; then
  echo "Terraform validation failed!"
  exit 1
fi
echo "Terraform validation successful."

# Generate a plan and check its output for expected ephemeral characteristics
echo "Generating Terraform plan and asserting ephemeral characteristics..."
PLAN_OUTPUT=$(terraform plan -input=false -out=tfplan -no-color)
if [ $? -ne 0 ]; then
  echo "Terraform plan failed!"
  echo "$PLAN_OUTPUT"
  exit 1
fi

# Assertions based on plan output
# Mock rationale: We are asserting that the *plan* contains specific configurations,
# not that actual cloud resources are created. This is deterministic and offline.

# Check for EC2 instance termination behavior
if ! echo "$PLAN_OUTPUT" | grep -q 'disable_api_termination = false'; then
  echo "Assertion failed: EC2 instance should allow API termination."
  exit 1
fi
if ! echo "$PLAN_OUTPUT" | grep -q 'instance_initiated_shutdown_behavior = "terminate"'; then
  echo "Assertion failed: EC2 instance should terminate on shutdown."
  exit 1
fi

# Check for S3 bucket lifecycle rule
if ! echo "$PLAN_OUTPUT" | grep -q 'expiration { days = 1 }'; then
  echo "Assertion failed: S3 bucket should have object expiration set to 1 day."
  exit 1
fi
if ! echo "$PLAN_OUTPUT" | grep -q 'versioning { enabled = false }'; then
  echo "Assertion failed: S3 bucket versioning should be disabled."
  exit 1
fi

# Check for RDS instance deletion protection and final snapshot
if ! echo "$PLAN_OUTPUT" | grep -q 'deletion_protection = false'; then
  echo "Assertion failed: RDS instance should not have deletion protection."
  exit 1
fi
if ! echo "$PLAN_OUTPUT" | grep -q 'skip_final_snapshot = true'; then
  echo "Assertion failed: RDS instance should skip final snapshot."
  exit 1
fi

echo "All ephemeral characteristics assertions passed!"

# Clean up plan file
rm tfplan

echo "Terraform module tests completed successfully."
