#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Use local backend and dummy AWS credentials to avoid real cloud calls.
# Initialize Terraform without a remote backend.
terraform init -backend=false > /dev/null

# Validate configuration syntax.
terraform validate

# Set mock AWS credentials for the provider (no actual network calls will be made).
export AWS_ACCESS_KEY_ID=mock
export AWS_SECRET_ACCESS_KEY=mock
export AWS_DEFAULT_REGION=us-east-1

# Run a deterministic plan with fixed variables.
terraform plan -input=false -out=plan.out \
  -var 'bucket_name=test-safehouse-bucket' \
  -var 'tags={}' \
  -var 'create_initial_object=false' \
  -var 'initial_object_content=Test' > /dev/null

echo "Tests passed"
