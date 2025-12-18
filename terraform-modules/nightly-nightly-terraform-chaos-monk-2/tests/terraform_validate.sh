#!/bin/bash

# Mock rationale: Test that the Terraform configuration is valid
set -e

echo "=== Testing Terraform Chaos Monkey Module ==="

echo "1. Validating Terraform syntax..."
terraform init -no-color > /dev/null 2>&1
terraform validate -no-color

echo "2. Testing safe mode configuration..."
cd examples/safe-mode
terraform init -no-color > /dev/null 2>&1
terraform plan -no-color -out=plan.out
echo "Safe mode plan generated successfully"

echo "3. Testing complete configuration..."
cd ../complete
terraform init -no-color > /dev/null 2>&1
terraform plan -no-color -out=plan.out
echo "Complete plan generated successfully"

echo "4. Checking outputs..."
terraform apply -no-color -auto-approve plan.out > /dev/null 2>&1
terraform output -json > outputs.json
cat outputs.json | grep -q "chaos_summary"
echo "Outputs validated successfully"

echo "=== All tests passed! ==="
