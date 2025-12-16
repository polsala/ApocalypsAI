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
    tag_key_prefix = "Nightly-"
    tags = merge(
      {
        ManagedBy = "ApocalypsAI"
        Project   = "ChaosGarden"
      },
      var.additional_tags
    )
  }
}

# Random provider for unique naming
provider "random" {
  # No configuration needed
}
