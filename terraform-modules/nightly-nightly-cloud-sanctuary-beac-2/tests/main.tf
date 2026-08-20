# Mock rationale: This configuration uses the module with dummy values
# to allow `terraform validate` and `terraform plan` to run offline
# without requiring actual AWS credentials or provisioning resources.
# The `aws` provider block is minimal and doesn't require authentication
# for `validate` or `plan` operations.

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
  region = "us-east-1" # Mock rationale: A default region is needed for provider configuration, but no actual API calls are made during plan/validate.
}

module "test_sanctuary_beacon" {
  source = "../src"

  bucket_name_prefix = "test-apocalypsai-beacon"
  domain_name        = "test.example.com" # Mock rationale: A dummy domain for testing the Route 53 resource creation logic.
  tags = {
    Environment = "Test"
    Purpose     = "ModuleTest"
  }
}

output "test_cloudfront_domain" {
  value = module.test_sanctuary_beacon.cloudfront_domain_name
}

output "test_s3_endpoint" {
  value = module.test_sanctuary_beacon.s3_bucket_website_endpoint
}
