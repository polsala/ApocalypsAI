#!/usr/bin/env bash
set -e

# Create a temporary test workspace
WORKDIR=$(mktemp -d)
cleanup() {
  rm -rf "$WORKDIR"
}
trap cleanup EXIT

# Write a minimal configuration that uses the module
cat > "$WORKDIR/main.tf" <<'EOF'
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = "us-east-1"
  skip_credentials_validation = true
  skip_requesting_account_id   = true
  # Dummy credentials to avoid real AWS calls
  access_key                  = "mock"
  secret_key                  = "mock"
  s3_use_path_style           = true
  endpoints {
    s3 = "http://localhost:4566"
  }
}

module "safehouse" {
  source      = "../../src"
  bucket_name = "test-safehouse-bucket"
}
EOF

# Initialize and validate
cd "$WORKDIR"
terraform init -backend=false -input=false > /dev/null
terraform validate -no-color

echo "✅ Terraform validation passed"
