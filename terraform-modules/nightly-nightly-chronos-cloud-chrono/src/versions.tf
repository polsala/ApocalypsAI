terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  # Mock rationale: For offline testing, credentials are not needed.
  # Terraform plan will simulate provider interactions.
  # In a real deployment, AWS credentials would be configured via environment variables or AWS CLI.
}
