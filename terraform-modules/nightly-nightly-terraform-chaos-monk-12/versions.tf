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
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment = terraform.workspace
      Purpose     = "chaos-engineering"
      ManagedBy   = "terraform-chaos-monkey"
      Project     = "apocalypsai"
    }
  }
}

provider "random" {
  # No special configuration needed
}
