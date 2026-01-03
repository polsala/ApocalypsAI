terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
}

# Provider configuration
provider "aws" {
  region = var.aws_region
  
  # Allow the provider to inherit credentials from environment variables
  # or IAM roles
}

# Backend configuration (optional, for remote state)
# terraform {
#   backend "s3" {
#     bucket = "my-terraform-state-bucket"
#     key    = "chaos-monkey/terraform.tfstate"
#     region = "us-east-1"
#   }
# }
