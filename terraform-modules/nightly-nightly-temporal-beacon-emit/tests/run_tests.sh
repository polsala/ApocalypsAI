#!/bin/bash
set -e

echo "Running Terraform module tests..."

# Test 1: Validate the module's HCL syntax
echo "Validating module source..."
terraform -chdir=../src init -backend=false -upgrade > /dev/null
terraform -chdir=../src validate

# Test 2: Check module formatting
echo "Checking module formatting..."
terraform -chdir=../src fmt -check -recursive

# Test 3: Validate the test instantiation's HCL syntax
echo "Validating test instantiation..."
terraform -chdir=. init -backend=false -upgrade > /dev/null
terraform -chdir=. validate

# Test 4: Check test instantiation formatting
echo "Checking test instantiation formatting..."
terraform -chdir=. fmt -check -recursive

# Test 5: Perform a dry run (plan) to ensure no errors and expected resource creation
# Mock rationale: This step generates a plan file without applying changes.
# It uses the 'mock_access_key' and 'mock_secret_key' in test_module.tf to satisfy
# the provider configuration, allowing the plan to be generated deterministically
# without actual AWS API calls. The focus is on the HCL's ability to form a valid plan.
echo "Performing dry run (plan) for test instantiation..."
terraform -chdir=. plan -out=tfplan -var="bucket_name_prefix=test-apocalypsai-beacon" -var="region=us-east-1" -var="environment=test"

# Test 6: Check plan output for expected resource creation (offline check)
# Mock rationale: This checks the *structure* of the plan output without actually
# interacting with AWS. It ensures the 'aws_s3_bucket.temporal_beacon' resource
# is part of the plan, indicating the module correctly defines the S3 bucket.
echo "Checking plan output for S3 bucket resource..."
if ! terraform -chdir=. show -json tfplan | grep -q 'aws_s3_bucket.temporal_beacon'; then
  echo "Error: aws_s3_bucket.temporal_beacon not found in plan!"
  exit 1
fi

# Clean up the generated plan file
rm tfplan

echo "All Terraform HCL validation, formatting, and plan structure tests passed successfully!"
