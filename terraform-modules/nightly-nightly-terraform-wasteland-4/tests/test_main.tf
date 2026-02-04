# Mock rationale: Terraform tests use local providers and isolated state to simulate cloud resources without real deployment.

provider "aws" {
  region                      = "us-test-1"
  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check    = true
  skip_requesting_account_id  = true

  endpoints {
    ec2 = "http://localhost:4566"
    s3  = "http://localhost:4566"
  }
}

terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

module "wasteland_shelter" {
  source = "../src"

  region       = "us-test-1"
  shelter_name = "test-shelter"
}

output "test_shelter_instance" {
  value = module.wasteland_shelter.shelter_instance
}

output "test_survival_bucket" {
  value = module.wasteland_shelter.survival_bucket
}
