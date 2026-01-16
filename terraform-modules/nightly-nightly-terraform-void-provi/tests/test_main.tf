# Mock rationale: We use local provider and mock resources to simulate AWS without real API calls.

provider "aws" {
  region                      = "us-test-1"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  s3_use_path_style           = true
  skip_requesting_account_id  = true
  access_key                  = "mock_access_key"
  secret_key                  = "mock_secret_key"

  endpoints {
    ec2    = "http://localhost:4566"
    s3     = "http://localhost:4566"
  }
}

terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

module "test_void_provisioner" {
  source = "../src"

  region         = "us-test-1"
  instance_count = 2
  bucket_name    = "test-survival-cache"
}

output "test_instance_ids" {
  value = module.test_void_provisioner.instance_ids
}

output "test_bucket_arn" {
  value = module.test_void_provisioner.bucket_arn
}

output "test_security_group_id" {
  value = module.test_void_provisioner.security_group_id
}
