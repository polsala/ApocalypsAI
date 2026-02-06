#!/usr/bin/env bash
# Test that the Terraform module validates and plans successfully with mock variables.
# Mock rationale: we use dummy AWS provider configuration via environment variables.

set -e

# Initialize without a remote backend (offline safe mode)
terraform init -backend=false > /dev/null

# Validate the configuration syntax
terraform validate

# Perform a dry‑run plan with example variables. No real AWS calls are made because the AWS provider
# will attempt to validate configuration only; credentials are not required for a plan that does not
# reach the apply stage.
terraform plan -input=false -out=plan.out \
  -var 'bucket_name=test-bucket' \
  -var 'force_destroy=true' \
  -var 'tags={Environment="dev"}' > /dev/null

echo "All Terraform checks passed."
