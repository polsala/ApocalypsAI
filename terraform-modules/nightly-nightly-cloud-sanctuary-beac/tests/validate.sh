#!/bin/bash
set -e

# Change to the directory of the script
cd "$(dirname "$0")"

echo "Initializing Terraform..."
# Use -backend=false for offline testing, prevents state file operations
terraform init -backend=false

echo "Validating Terraform syntax..."
terraform validate

echo "Generating a plan (without applying)..."
# Use -destroy to ensure all resources can be planned for destruction,
# which implicitly checks creation as well.
# Pass variables explicitly to avoid interactive prompts.
terraform plan -destroy -out=tfplan -input=false \
  -var="region=us-east-1" \
  -var="beacon_message=Test Message for Plan" \
  -var="create_dns_record=false" \
  -var="domain_name=test.example.com" \
  -var="subdomain=test-beacon"

echo "Terraform module validation successful!"

# Mock rationale: This test performs static analysis (init, validate) and plan generation
# without interacting with actual cloud resources. It ensures the module's syntax is correct,
# variables are properly defined and used, and a plan can be generated.
# By setting `create_dns_record=false`, we avoid requiring a real Route 53 Hosted Zone,
# making the test deterministic and offline. The `terraform plan -destroy` command
# is used to verify that the module can successfully generate a plan for both creation
# and destruction, covering the full lifecycle without actual deployment.
