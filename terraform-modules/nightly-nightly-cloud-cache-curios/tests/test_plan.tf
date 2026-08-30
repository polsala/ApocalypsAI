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

# Mock rationale: This configuration acts as a mock for a real-world deployment.
# It uses the module with specific, controlled inputs to ensure the module's
# internal logic and resource definitions are syntactically correct and produce
# a predictable plan without requiring actual cloud credentials or resource provisioning.
# The 'terraform plan' command run by the test script will validate this.

provider "aws" {
  region = "us-east-1" # Mock region, not actually used for provisioning
  # No actual credentials needed for 'terraform plan' validation
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "test_curiosity_cache" {
  source = "../src" # Path to the module being tested

  bucket_name_prefix    = "test-curios"
  retention_days        = 90
  transition_to_ia_days = 15
  tags = {
    Environment = "Test"
    Owner       = "ApocalypsAI"
  }
}

output "test_bucket_id" {
  value = module.test_curiosity_cache.bucket_id
}

output "test_bucket_arn" {
  value = module.test_curiosity_cache.bucket_arn
}
