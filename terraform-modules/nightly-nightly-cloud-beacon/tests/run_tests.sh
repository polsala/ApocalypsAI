#!/bin/bash
set -e

echo "Running Nightly Cloud Beacon module tests..."

# Initialize Terraform in the tests directory.
# -backend=false prevents Terraform from trying to configure a backend,
# which is not needed for local validation and planning.
terraform -chdir=tests init -backend=false

# Validate the Terraform configuration for syntax and consistency.
# Mock rationale: `terraform validate` performs a static analysis of the
# configuration files, checking for syntax errors, argument types, and
# variable references without interacting with any cloud provider APIs.
terraform -chdir=tests validate

# Perform a dry run to ensure the plan can be generated without errors.
# -out=/dev/null discards the plan file, as we only care about successful generation.
# -input=false prevents interactive prompts.
# Mock rationale: `terraform plan` generates an execution plan based on the
# configuration, simulating resource creation/modification. This step does not
# provision actual cloud resources and can be run offline to verify the module's
# logic and resource definitions are sound.
terraform -chdir=tests plan -out=/dev/null -input=false

echo "All Nightly Cloud Beacon module tests passed successfully!"
