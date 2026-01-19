# Mock rationale: This test uses terraform init and plan to validate the module structure without provisioning real resources.

provider "aws" {
  region = "us-west-2"
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

module "test_outpost" {
  source         = "../src"
  region         = "us-west-2"
  outpost_name   = "test-outpost"
  instance_count = 2
}

output "test_vpc_id" {
  value = module.test_outpost.vpc_id
}

output "test_public_ips" {
  value = module.test_outpost.public_ips
}
