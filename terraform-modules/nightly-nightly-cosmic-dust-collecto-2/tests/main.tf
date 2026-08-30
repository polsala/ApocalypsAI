# Mock rationale: This configuration uses the module with dummy inputs
# to allow for offline validation and planning without actual cloud deployment.
# It simulates how a user would consume the module.

provider "aws" {
  region = "us-east-1"
  # Mock rationale: Dummy credentials for offline testing.
  # Terraform validate and plan do not require actual credentials.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

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

module "test_cosmic_dust_collector" {
  source = "../src" # Path to the module being tested

  bucket_name_prefix = "test-apocalypsai-dust"
  environment        = "test"
  tags = {
    Project = "ApocalypsAI"
    Test    = "True"
  }
}

output "test_bucket_id" {
  value = module.test_cosmic_dust_collector.bucket_id
}

output "test_log_group_name" {
  value = module.test_cosmic_dust_collector.log_group_name
}
