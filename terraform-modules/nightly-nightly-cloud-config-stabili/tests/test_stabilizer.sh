#!/bin/bash
set -euo pipefail

# Mock rationale: This test script simulates Terraform operations locally
# without interacting with a real cloud provider. It uses a temporary
# directory and controls input variables to deterministically test
# the module's behavior under "stable" and "drifted" conditions.
# The 'local-exec' provisioner within the module itself contains the
# core mocking logic for drift detection.

TEMP_DIR=$(mktemp -d)
echo "Using temporary directory: $TEMP_DIR"
cd "$TEMP_DIR"

# Create a minimal Terraform configuration to use the module
cat <<EOF > main.tf
provider "aws" {
  region = "us-east-1" # Mock region, not actually used
  # Mock rationale: The AWS provider is declared but not configured with
  # credentials, ensuring no actual cloud interaction. The module's
  # functionality for this test relies on the 'null_resource' and its
  # 'local-exec' provisioner, which is fully self-contained.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "stabilizer" {
  source = "../src"
  bucket_name = "test-apocalypsai-archive-$(date +%s)"
  simulate_drift_signal = var.drift_signal_input
}

variable "drift_signal_input" {
  type = string
}
EOF

echo "-- Initializing Terraform --"
terraform init -backend=false > /dev/null
if [ $? -ne 0 ]; then
    echo "FAIL: Terraform init failed!"
    exit 1
fi

echo "-- Test Case 1: Stable Configuration --"
# Run plan with 'STABLE' signal
PLAN_OUTPUT=$(terraform plan -no-color -detailed-exitcode -var="drift_signal_input=STABLE" 2>&1)
PLAN_EXIT_CODE=$?

echo "$PLAN_OUTPUT"
if [ $PLAN_EXIT_CODE -eq 0 ]; then
    echo "PASS: Stable configuration detected (exit code 0)."
    if echo "$PLAN_OUTPUT" | grep -q "is stable. No configuration rifts detected."; then
        echo "PASS: Stable message found in output."
    else
        echo "FAIL: Stable message NOT found in output."
        exit 1
    fi
else
    echo "FAIL: Expected exit code 0 for stable configuration, got $PLAN_EXIT_CODE."
    exit 1
fi

echo "-- Test Case 2: Drift Detected Configuration --"
# Run plan with 'DRIFT_DETECTED' signal
PLAN_OUTPUT=$(terraform plan -no-color -detailed-exitcode -var="drift_signal_input=DRIFT_DETECTED" 2>&1)
PLAN_EXIT_CODE=$?

echo "$PLAN_OUTPUT"
# When the local-exec provisioner exits with 1 (indicating a problem),
# terraform plan will also exit with 1 (error).
if [ $PLAN_EXIT_CODE -eq 1 ]; then
    echo "PASS: Drift detected and reported as an error (exit code 1)."
    if echo "$PLAN_OUTPUT" | grep -q "WARNING: Configuration Rift Detected!"; then
        echo "PASS: Drift warning message found in output."
    else
        echo "FAIL: Drift warning message NOT found in output."
        exit 1
    fi
else
    echo "FAIL: Expected exit code 1 for drift detected, got $PLAN_EXIT_CODE."
    exit 1
fi

echo "-- Cleaning up temporary directory --"
rm -rf "$TEMP_DIR"
echo "All tests passed!"
