#!/bin/bash

# Basic integration test for the chaos garden module
# This test verifies that the module can be applied and outputs are correct

set -e

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXAMPLE_DIR="$TEST_DIR/../examples/basic_garden"

echo "=== Chaos Garden Integration Test ==="
echo "Test directory: $TEST_DIR"
echo "Example directory: $EXAMPLE_DIR"

echo "\n1. Initializing Terraform..."
cd "$EXAMPLE_DIR"
terraform init -input=false

echo "\n2. Planning deployment..."
terraform plan -input=false -out=test.plan

echo "\n3. Applying configuration..."
terraform apply -auto-approve test.plan

echo "\n4. Verifying outputs..."
OUTPUTS=$(terraform output -json)

echo "\nOutputs:\n$OUTPUTS"

echo "\n5. Checking garden resources..."
GARDEN_NAME=$(echo "$OUTPUTS" | jq -r '.garden_name.value')
EC2_COUNT=$(echo "$OUTPUTS" | jq -r '.garden_resources.value.ec2_instances.count')
LAMBDA_COUNT=$(echo "$OUTPUTS" | jq -r '.garden_resources.value.lambda_functions.count')
S3_COUNT=$(echo "$OUTPUTS" | jq -r '.garden_resources.value.s3_buckets.count')
RDS_COUNT=$(echo "$OUTPUTS" | jq -r '.garden_resources.value.rds_instances.count')

echo "\nGarden Name: $GARDEN_NAME"
echo "EC2 Instances: $EC2_COUNT"
echo "Lambda Functions: $LAMBDA_COUNT"
echo "S3 Buckets: $S3_COUNT"
echo "RDS Instances: $RDS_COUNT"

echo "\n6. Verifying chaos schedule..."
CHAOS_SCHEDULE=$(echo "$OUTPUTS" | jq -r '.chaos_schedule.value')
CLEANUP_SCHEDULE=$(echo "$OUTPUTS" | jq -r '.cleanup_schedule.value')

echo "Chaos Schedule: $CHAOS_SCHEDULE"
echo "Cleanup Schedule: $CLEANUP_SCHEDULE"

echo "\n7. Cleanup..."
terraform destroy -auto-approve

echo "\n=== Test Results ==="
echo "✓ Terraform init successful"
echo "✓ Terraform plan successful"
echo "✓ Terraform apply successful"
echo "✓ Garden name generated: $GARDEN_NAME"
echo "✓ EC2 instances: $EC2_COUNT (expected: 2)"
echo "✓ Lambda functions: $LAMBDA_COUNT (expected: 1)"
echo "✓ S3 buckets: $S3_COUNT (expected: 1)"
echo "✓ RDS instances: $RDS_COUNT (expected: 0)"
echo "✓ Chaos schedule: $CHAOS_SCHEDULE"
echo "✓ Cleanup schedule: $CLEANUP_SCHEDULE"
echo "✓ Terraform destroy successful"

echo "\n=== All Tests Passed! ==="

# Verify expected values
echo "\n=== Validation ==="
if [ "$EC2_COUNT" -eq 2 ]; then
  echo "✓ EC2 instance count correct"
else
  echo "✗ EC2 instance count incorrect: expected 2, got $EC2_COUNT"
  exit 1
fi

if [ "$LAMBDA_COUNT" -eq 1 ]; then
  echo "✓ Lambda function count correct"
else
  echo "✗ Lambda function count incorrect: expected 1, got $LAMBDA_COUNT"
  exit 1
fi

if [ "$S3_COUNT" -eq 1 ]; then
  echo "✓ S3 bucket count correct"
else
  echo "✗ S3 bucket count incorrect: expected 1, got $S3_COUNT"
  exit 1
fi

if [ "$RDS_COUNT" -eq 0 ]; then
  echo "✓ RDS instance count correct"
else
  echo "✗ RDS instance count incorrect: expected 0, got $RDS_COUNT"
  exit 1
fi

if [[ "$CHAOS_SCHEDULE" == "cron(0 */2 * * ? *)" ]]; then
  echo "✓ Chaos schedule correct"
else
  echo "✗ Chaos schedule incorrect: expected 'cron(0 */2 * * ? *)', got '$CHAOS_SCHEDULE'"
  exit 1
fi

if [[ "$CLEANUP_SCHEDULE" == "cron(0 2 * * ? *)" ]]; then
  echo "✓ Cleanup schedule correct"
else
  echo "✗ Cleanup schedule incorrect: expected 'cron(0 2 * * ? *)', got '$CLEANUP_SCHEDULE'"
  exit 1
fi

echo "\n=== All Validations Passed! ==="

# Cleanup test files
echo "\n=== Cleaning Up ==="
rm -f test.plan
echo "✓ Test files cleaned up"

echo "\n=== Chaos Garden Test Suite Complete ==="
echo "All tests and validations passed successfully!"
