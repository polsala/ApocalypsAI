terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }
}

# Provider configuration
provider "aws" {
  region = var.region
  
  # Enable retries for transient failures
  skip_credentials_validation = false
  skip_metadata_api_check    = false
  skip_region_validation     = false
  skip_requesting_account_id = false
  
  # Configure retries
  max_retries = 5
}

# Configure random provider
provider "random" {
  # No special configuration needed
}

# Backend configuration (optional)
# terraform {
#   backend "s3" {
#     bucket         = "my-terraform-state"
#     key            = "chaos-monkey/terraform.tfstate"
#     region         = "us-east-1"
#     encrypt        = true
#     dynamodb_table = "my-terraform-locks"
#   }
# }
