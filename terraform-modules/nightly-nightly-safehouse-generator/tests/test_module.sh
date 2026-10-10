#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Use a temporary directory to avoid polluting the repository
TMPDIR=$(mktemp -d)
cd "$TMPDIR"

# Copy module files into the temp directory
cp -r "$OLDPWD"/* .

# Initialize Terraform (disable remote backend)
terraform init -backend=false > /dev/null

# Validate configuration syntax
terraform validate

# Apply the module automatically
terraform apply -auto-approve -input=false > apply.log

# Retrieve the safehouse path output
SAFEHOUSE_PATH=$(terraform output -raw safehouse_path)

# Verify that the safehouse file exists
if [[ -f "$SAFEHOUSE_PATH" ]]; then
  echo "✅ Safehouse file exists: $SAFEHOUSE_PATH"
else
  echo "❌ Safehouse file not found"
  exit 1
fi

# Clean up resources
terraform destroy -auto-approve -input=false > /dev/null
rm -rf "$TMPDIR"
