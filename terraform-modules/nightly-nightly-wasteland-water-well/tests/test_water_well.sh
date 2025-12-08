#!/bin/bash

# Mock rationale: Validate Terraform syntax and output structure without cloud resources

set -e

terraform init -backend=false

terraform validate

terraform plan -out=test.plan

terraform show test.plan | grep -q "well_name = \"oasis-1\""

terraform show test.plan | grep -q "capacity_liters = 1000"

terraform show test.plan | grep -q "alert_threshold = 200"

echo "Water well test passed!"

# Cleanup
terraform destroy -auto-approve
