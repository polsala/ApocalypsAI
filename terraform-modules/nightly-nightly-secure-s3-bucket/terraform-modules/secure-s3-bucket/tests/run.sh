#!/usr/bin/env bash
set -euo pipefail

# Create a temporary working directory
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

# Copy module files
cp -r "$(dirname "$0")/../src" "$TMPDIR/module"

# Write a minimal root configuration that consumes the module
cat > "$TMPDIR/main.tf" <<'EOF'
module "test_bucket" {
  source        = "./module"
  bucket_prefix = "test"
  tags = {
    Purpose = "unit-test"
  }
  aws_region = "us-east-1"
}
EOF

cd "$TMPDIR"
# Initialise Terraform without a backend (offline only)
terraform init -backend=false > /dev/null
# Validate configuration – should succeed without contacting AWS
terraform validate

echo "Tests passed"
