# Mock rationale: This test configuration instantiates the module
# to allow `terraform validate` and `terraform plan` to check its syntax
# and planned resource creation without requiring actual AWS credentials.
# The `aws` provider block is minimal and doesn't need real credentials for `validate` or `plan`.
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
  region = "us-east-1" # Mock region for validation
  # access_key = "mock_access_key" # Not strictly needed for validate/plan
  # secret_key = "mock_secret_key" # Not strictly needed for validate/plan
}

module "test_ephemeral_bucket" {
  source = "../src" # Path to the module under test
  
  resource_name_prefix = "test-cauldron"
  region               = "us-east-1"
  ttl_days             = 3
  tags = {
    TestEnv = "True"
  }
}

output "test_bucket_id" {
  value = module.test_ephemeral_bucket.bucket_id
}

output "test_bucket_arn" {
  value = module.test_ephemeral_bucket.bucket_arn
}
