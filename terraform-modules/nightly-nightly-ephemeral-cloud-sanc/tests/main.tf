terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  # Mock rationale: For offline testing, we don't need actual credentials.
  # Terraform validate and plan -destroy will work without them,
  # as long as the provider is declared. The values are placeholders.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "ephemeral_sanctuary_test" {
  source = "../src"

  project_name    = "test-apocalypsai"
  aws_region      = "us-east-1"
  vpc_cidr_block  = "10.10.0.0/16"
  subnet_cidr_block = "10.10.1.0/24"
}
