#!/usr/bin/env bash
set -e

# Mock rationale: using local backend and dummy provider to validate syntax only.
# Initialise Terraform without a remote backend.
terraform init -backend=false > /dev/null

# Validate the configuration.
terraform validate

# Provide a dummy variable file for planning.
cat > terraform.tfvars <<EOF
bucket_name = "example-safehouse"
EOF

# Run a plan; we do not apply, just ensure it succeeds.
terraform plan -var-file=terraform.tfvars -out=plan.out > /dev/null

echo "Tests passed"
