#!/bin/bash

set -euo pipefail

# Mock rationale: These tests are designed to be offline and deterministic.
# They do not require actual AWS credentials or network access beyond initial provider download.
# `terraform init` will download providers if not cached, but subsequent `validate` and `plan`
# operations are purely based on HCL syntax and local state. The `data "aws_caller_identity"`
# will show as `(known after apply)` in the plan, which is expected and does not prevent testing
# the module's structure.

echo "Running Terraform module tests..."

# Initialize Terraform in the test directory
terraform -chdir=tests init -backend=false # Mock rationale: -backend=false prevents state backend configuration, making it purely local.

# Validate the Terraform configuration
echo "\n--- Running terraform validate ---"
terraform -chdir=tests validate
if [ $? -ne 0 ]; then
  echo "ERROR: Terraform validation failed!"
  exit 1
fi
echo "Terraform validation passed."

# Generate a plan and check for expected resources
echo "\n--- Running terraform plan ---"
PLAN_OUTPUT=$(terraform -chdir=tests plan -target=module.temporal_echo_chamber -no-color)

# Check for the creation of the main SQS queue
echo "Checking for main SQS queue..."
echo "${PLAN_OUTPUT}" | grep -q 'aws_sqs_queue.temporal_echo_chamber_queue'
if [ $? -ne 0 ]; then
  echo "ERROR: Main SQS queue not found in plan!"
  exit 1
fi
echo "Main SQS queue found."

# Check for the creation of the DLQ
echo "Checking for DLQ..."
echo "${PLAN_OUTPUT}" | grep -q 'aws_sqs_queue.temporal_echo_chamber_dlq'
if [ $? -ne 0 ]; then
  echo "ERROR: DLQ not found in plan!"
  exit 1
fi
echo "DLQ found."

# Check for the creation of the S3 archive bucket
echo "Checking for S3 archive bucket..."
echo "${PLAN_OUTPUT}" | grep -q 'aws_s3_bucket.temporal_echo_archive_bucket'
if [ $? -ne 0 ]; then
  echo "ERROR: S3 archive bucket not found in plan!"
  exit 1
fi
echo "S3 archive bucket found."

# Check for S3 public access block
echo "Checking for S3 public access block..."
echo "${PLAN_OUTPUT}" | grep -q 'aws_s3_bucket_public_access_block.temporal_echo_archive_bucket_public_access_block'
if [ $? -ne 0 ]; then
  echo "ERROR: S3 public access block not found in plan!"
  exit 1
fi
echo "S3 public access block found."

# Check for S3 versioning
echo "Checking for S3 versioning..."
echo "${PLAN_OUTPUT}" | grep -q 'aws_s3_bucket_versioning.temporal_echo_archive_bucket_versioning'
if [ $? -ne 0 ]; then
  echo "ERROR: S3 versioning not found in plan!"
  exit 1
fi
echo "S3 versioning found."

echo "\nAll Terraform module tests passed successfully!"
