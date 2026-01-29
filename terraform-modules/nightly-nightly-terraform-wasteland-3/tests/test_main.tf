# Mock rationale: Terraform tests use local providers and ephemeral state to simulate infrastructure without real cloud costs.

provider "aws" {
  region                      = "us-test-1"
  skip_credentials_validation = true
  skip_requesting_account_id  = true
  access_key                  = "mock_access_key"
  secret_key                  = "mock_secret_key"
}

module "test_shelter" {
  source = "../src"

  region           = "us-test-1"
  shelter_name     = "test-shelter"
  instance_type    = "t3.micro"
  db_instance_class = "db.t3.micro"
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

output "test_shelter_ip" {
  value = module.test_shelter.shelter_ip
}

output "test_db_endpoint" {
  value = module.test_shelter.db_endpoint
}

output "test_vpc_id" {
  value = module.test_shelter.vpc_id
}
