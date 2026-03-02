#!/bin/bash
set -euo pipefail

echo "--- Running Terraform module tests ---"

# Mock rationale: terraform init -backend=false prevents any interaction with remote state backends,
# making the initialization purely local and deterministic.
echo "Initializing Terraform (local only)..."
terraform -chdir=./ init -backend=false

# Mock rationale: terraform validate checks configuration syntax and internal consistency
# without requiring any cloud API calls. It's fully offline.
echo "Validating Terraform configuration..."
terraform -chdir=./ validate

# Mock rationale: terraform plan generates an execution plan.
# The -out=tfplan flag saves the plan to a local file and prevents actual application.
# It does not interact with AWS APIs when providers are mocked or when only syntax/graph is checked.
# For a module, it ensures the module can be successfully planned with given inputs.
echo "Generating Terraform plan (dry run)..."
terraform -chdir=./ plan -out=tfplan -var="bucket_name_prefix=test-dust" -var="environment=test" -var="tags={Project=ApocalypsAI}"

echo "Cleaning up generated plan file..."
rm tfplan

echo "--- Terraform module tests PASSED ---"
