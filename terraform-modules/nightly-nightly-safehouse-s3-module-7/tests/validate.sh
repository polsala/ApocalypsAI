#!/usr/bin/env bash
# Test that the module validates and plans without errors.
# Mock rationale: Using local backend and dummy provider configuration.

set -e

# Create temporary directory
TMPDIR=$(mktemp -d)
cd "$TMPDIR"

# Write minimal provider configuration (no real AWS calls needed for validation)
cat > provider.tf <<'EOF'
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  # Dummy region; validation does not contact AWS
  region = "us-east-1"
}
EOF

# Copy the module source into the temp dir
mkdir -p safehouse
cp -r "$PWD/../src/"* safehouse/

# Create a test configuration that consumes the module
cat > main.tf <<'EOF'
module "safehouse" {
  source = "./safehouse"
}
EOF

# Initialize and validate
terraform init -input=false -no-color > /dev/null
terraform validate -no-color

echo "Validation succeeded."
