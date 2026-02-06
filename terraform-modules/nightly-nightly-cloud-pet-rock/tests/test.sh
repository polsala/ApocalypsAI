#!/bin/bash

set -e # Exit immediately if a command exits with a non-zero status.

echo "--- Running Terraform tests for nightly-cloud-pet-rock ---"

# Change to the tests directory
cd "$(dirname "$0")"

# Initialize Terraform
echo "Initializing Terraform..."
terraform init -backend=false # Mock rationale: No actual backend needed for plan validation.

# Test case 1: Basic pet rock deployment (no website hosting)
echo "Running terraform plan for basic pet rock..."
terraform plan -var="bucket_name_prefix=test-basic" -var="enable_website_hosting=false" -out=tfplan_basic -no-color
if [ $? -ne 0 ]; then
  echo "ERROR: Terraform plan for basic pet rock failed."
  exit 1
fi
echo "Terraform plan for basic pet rock successful."
# Check for expected resources in the plan output (offline check)
if ! grep -q "aws_s3_bucket.pet_rock_bucket" tfplan_basic; then
  echo "ERROR: aws_s3_bucket.pet_rock_bucket not found in basic plan."
  exit 1
fi
if grep -q "aws_s3_bucket_website_configuration.pet_rock_bucket_website" tfplan_basic; then
  echo "ERROR: aws_s3_bucket_website_configuration.pet_rock_bucket_website found in basic plan (should not be)."
  exit 1
fi
if grep -q "aws_s3_bucket_policy.pet_rock_bucket_policy" tfplan_basic; then
  echo "ERROR: aws_s3_bucket_policy.pet_rock_bucket_policy found in basic plan (should not be)."
  exit 1
fi
if grep -q "aws_s3_bucket_ownership_controls.pet_rock_bucket_ownership" tfplan_basic; then
  echo "ERROR: aws_s3_bucket_ownership_controls.pet_rock_bucket_ownership found in basic plan (should not be)."
  exit 1
fi
rm tfplan_basic # Clean up plan file

# Test case 2: Pet rock with website hosting enabled
echo "Running terraform plan for pet rock with website hosting..."
terraform plan -var="bucket_name_prefix=test-website" -var="enable_website_hosting=true" -out=tfplan_website -no-color
if [ $? -ne 0 ]; then
  echo "ERROR: Terraform plan for pet rock with website hosting failed."
  exit 1
fi
echo "Terraform plan for pet rock with website hosting successful."
# Check for expected resources in the plan output (offline check)
if ! grep -q "aws_s3_bucket.pet_rock_bucket" tfplan_website; then
  echo "ERROR: aws_s3_bucket.pet_rock_bucket not found in website plan."
  exit 1
fi
if ! grep -q "aws_s3_bucket_website_configuration.pet_rock_bucket_website" tfplan_website; then
  echo "ERROR: aws_s3_bucket_website_configuration.pet_rock_bucket_website not found in website plan."
  exit 1
fi
if ! grep -q "aws_s3_bucket_policy.pet_rock_bucket_policy" tfplan_website; then
  echo "ERROR: aws_s3_bucket_policy.pet_rock_bucket_policy not found in website plan."
  exit 1
fi
if ! grep -q "aws_s3_bucket_ownership_controls.pet_rock_bucket_ownership" tfplan_website; then
  echo "ERROR: aws_s3_bucket_ownership_controls.pet_rock_bucket_ownership not found in website plan."
  exit 1
fi
rm tfplan_website # Clean up plan file

echo "All Terraform tests passed successfully!"
