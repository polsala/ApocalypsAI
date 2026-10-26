# Mock rationale: This configuration is purely for validating the module's syntax
# and variable definitions. It uses a 'null_resource' (implicitly, by not provisioning
# anything beyond the module itself) to avoid actual cloud provisioning and ensures
# 'terraform validate' can run deterministically offline. The 'aws' provider is
# declared but not configured with credentials, as validate only checks syntax and
# schema, not live API calls.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0" # Specify a compatible version
    }
  }
}

provider "aws" {
  # No actual credentials needed for 'terraform validate' on module syntax.
  # This block is just to satisfy the provider requirement for the module.
  region = "us-east-1" # A dummy region is fine for validation.
}

module "test_chrono_vault" {
  source = "../../src" # Path to the module being tested

  bucket_name          = "test-chrono-vault-bucket-12345"
  temporal_stasis_days = 7
  entropic_decay_days  = 14
  tags = {
    Environment = "Test"
    Project     = "ApocalypsAI"
  }
}

# An additional test case for null entropic_decay_days
module "test_chrono_vault_no_decay" {
  source = "../../src"

  bucket_name          = "test-chrono-vault-no-decay-67890"
  temporal_stasis_days = 60
  entropic_decay_days  = null # Test the null case
}

output "test_bucket_id" {
  value = module.test_chrono_vault.bucket_id
}

output "test_bucket_arn" {
  value = module.test_chrono_vault.bucket_arn
}
