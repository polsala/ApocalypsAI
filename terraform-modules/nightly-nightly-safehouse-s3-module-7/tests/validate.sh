#!/usr/bin/env bash
# Mock rationale: This script runs entirely offline using the local backend.
# It ensures the module syntax is valid without contacting AWS.

set -euo pipefail

# Create a temporary working directory
TMPDIR=$(mktemp -d)
cp -r . "$TMPDIR/module"
cd "$TMPDIR/module"

# Write a minimal root configuration that consumes the module
cat > main.tf <<'EOF'
module "test_safehouse" {
  source      = "./src"
  bucket_name = "test-safehouse-bucket"
  tags = {
    Environment = "test"
  }
}
EOF

# Initialise Terraform with a local backend and a dummy AWS provider configuration
export AWS_ACCESS_KEY_ID="dummy"
export AWS_SECRET_ACCESS_KEY="dummy"
export AWS_ENDPOINT_URL="http://localhost:4566" # No actual service; provider will fail only on apply

terraform init -backend=false -input=false > /dev/null

echo "Running terraform validate..."
terraform validate

echo "✅ Validation succeeded"

# Clean up
rm -rf "$TMPDIR"
