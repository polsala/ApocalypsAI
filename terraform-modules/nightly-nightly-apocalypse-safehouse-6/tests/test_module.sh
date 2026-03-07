#!/usr/bin/env bash
set -e

# Create temporary working directory
TMPDIR=$(mktemp -d)
cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

# Write minimal configuration that uses the module
cat > "$TMPDIR/main.tf" <<'EOF'
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
  region                      = "us-east-1"
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true
  endpoints {
    s3 = "http://localhost:4566"
  }
}

module "safehouse" {
  source = "../.."
}
EOF

# Initialize and validate
terraform -chdir="$TMPDIR" init -backend=false -input=false > /dev/null
terraform -chdir="$TMPDIR" validate -no-color

echo "Terraform module validation passed."

# Mock rationale: The test runs entirely offline using the AWS provider's ability to skip credential validation and a dummy local endpoint.
