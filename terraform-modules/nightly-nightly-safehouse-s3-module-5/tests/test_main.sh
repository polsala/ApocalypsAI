#!/usr/bin/env bash
set -e

# Mock rationale: Use a temporary directory to init and validate the module without real AWS credentials.
TMPDIR=$(mktemp -d)

# Copy module source
cp -r "$(dirname "$0")/../src" "$TMPDIR/src"

# Create a minimal root configuration that consumes the module
cat > "$TMPDIR/main.tf" <<'EOF'
module "safehouse" {
  source      = "./src"
  bucket_name = "apocalypse-safehouse-test"
}
EOF

cd "$TMPDIR"

# Initialize Terraform (backend disabled to avoid remote state requirements)
terraform init -backend=false -input=false > /dev/null

# Validate configuration syntax and provider requirements
terraform validate

echo "Terraform validation passed."

# Ensure expected outputs are defined (mock rationale: we only check that the output names exist)
terraform output -json | grep -q '"bucket_arn"' || { echo "Missing bucket_arn output"; exit 1; }
terraform output -json | grep -q '"vault_password"' || { echo "Missing vault_password output"; exit 1; }

echo "All expected outputs are present."
