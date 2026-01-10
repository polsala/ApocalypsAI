#!/bin/bash

set -euo pipefail

echo "Running offline tests for nightly-ephemeral-echo-vault..."

# Change to the tests directory
cd "$(dirname "$0")"

# Initialize Terraform (downloads providers, sets up backend)
# Mock rationale: `terraform init` downloads necessary provider plugins but does not make API calls
# to AWS if no backend is configured or if the configuration is purely local.
# The -backend=false flag ensures no remote state operations are attempted.
terraform init -backend=false

# Validate the Terraform configuration syntax and semantics
echo "\n--- Running terraform validate ---"
terraform validate

# Generate a plan to ensure the module can be planned for creation
# Mock rationale: `terraform plan` generates an execution plan based on the local configuration
# and a simulated state. It does not interact with actual cloud resources without an `apply`.
# No AWS credentials are required for this step to succeed for a basic plan.
echo "\n--- Running terraform plan (creation) ---"
terraform plan -out=tfplan_create

# Generate a plan to ensure the module can be planned for destruction
# This is crucial for a 'decay chamber' to ensure it can be torn down.
# Mock rationale: `terraform plan -destroy` simulates the destruction of resources.
# Like `terraform plan`, it operates on local configuration and simulated state.
echo "\n--- Running terraform plan (destruction) ---"
terraform plan -destroy -out=tfplan_destroy

# Clean up generated plan files
rm tfplan_create tfplan_destroy

echo "\nAll offline tests passed successfully!"
