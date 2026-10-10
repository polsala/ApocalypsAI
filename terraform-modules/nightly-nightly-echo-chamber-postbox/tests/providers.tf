terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  # Mock rationale: For offline testing, we don't need actual credentials.
  # Terraform plan/validate will still work without them for syntax and graph checks.
  # Setting dummy values to satisfy provider configuration requirements.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}
