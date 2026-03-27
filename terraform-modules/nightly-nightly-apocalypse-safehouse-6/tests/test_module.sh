#!/usr/bin/env bash
set -e

# Mock rationale: Use a local backend and dummy AWS provider configuration to validate the module without real AWS credentials.

cat > provider.tf <<'EOF'
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}
provider "aws" {
  region                      = "us-east-1"
  access_key                  = "mock_access_key"
  secret_key                  = "mock_secret_key"
  skip_credentials_validation = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true
  endpoints {
    s3 = "http://localhost:4566"
  }
}
EOF

terraform init -backend=false > /dev/null
terraform validate
terraform plan -input=false -var 'bucket_name=test-safehouse' > /dev/null

echo "All tests passed."
