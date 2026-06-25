terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1" # Mock rationale: Required for terraform validate to parse provider block, actual credentials not needed for syntax check.
  # No credentials configured here, as this is for offline validation only.
  # Running `terraform apply` would require AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, etc.
}
