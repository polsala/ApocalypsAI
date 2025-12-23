#!/usr/bin/env bash
# Mock rationale: This script assumes Terraform is installed in the environment.
# It runs init (without a backend) and validate on an example configuration.
set -e

# Create a temporary working directory
TMPDIR=$(mktemp -d)
cp -r $(dirname "$0")/../src "$TMPDIR/module"

cat > "$TMPDIR/main.tf" <<'EOF'
module "static_website" {
  source = "./module"
  bucket_name = "example-bucket-$(date +%s)"
  enable_cloudfront = false
}
EOF

cd "$TMPDIR"
terraform init -backend=false > /dev/null
terraform validate

if [ $? -eq 0 ]; then
  echo "Terraform validation succeeded."
  exit 0
else
  echo "Terraform validation failed."
  exit 1
fi
