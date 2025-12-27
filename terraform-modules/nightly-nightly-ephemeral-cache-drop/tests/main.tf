# Mock rationale: For offline testing of a Terraform module,
# we only need to validate the configuration and generate a plan.
# An actual AWS provider configuration is not required for these steps,
# as no real API calls are made. The provider blocks are included to satisfy
# Terraform's syntax requirements.
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
  region = "us-east-1"
  # No credentials needed for terraform validate and terraform plan
  # when testing a module's syntax and logic.
}

provider "random" {} # No specific configuration needed for random provider

module "ephemeral_cache_test" {
  source = "../" # Refers to the parent module
  
  bucket_name_prefix = "test-apocalypsai-drop"
  expiration_days    = 2
  tags = {
    TestRun = "true"
    Purpose = "ModuleTest"
  }
}

output "test_bucket_id" {
  value = module.ephemeral_cache_test.bucket_id
}

output "test_bucket_arn" {
  value = module.ephemeral_cache_test.bucket_arn
}
