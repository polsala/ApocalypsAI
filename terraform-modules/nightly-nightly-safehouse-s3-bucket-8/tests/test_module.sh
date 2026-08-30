#!/usr/bin/env bash
set -e

# Mock rationale: Use local backend and mock AWS credentials so the test runs without network access.
# Initialise the module (no remote backend)
terraform -chdir=../src init -backend=false > /dev/null

# Validate syntax and configuration
terraform -chdir=../src validate

# Run a mock plan with a dummy bucket name; this will succeed because credentials are mocked.
terraform -chdir=../src plan -var 'bucket_name=test-safehouse-bucket' -out=plan.out > /dev/null

# If we reached this point, the module passed all checks.
echo "PASS"
