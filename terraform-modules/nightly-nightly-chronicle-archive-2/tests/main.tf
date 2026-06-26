provider "aws" {
  region = var.region
  # Mock rationale: For offline testing, no actual AWS credentials are required for `terraform validate` and `terraform plan`.
  # The provider block is present for HCL syntax validation, but no API calls are made during the test script execution.
  # Dummy values are provided for `access_key` and `secret_key` to satisfy Terraform's provider configuration requirements
  # without needing actual credentials for these offline operations.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "chronicle_archive_test" {
  source = "../src"

  bucket_name = var.bucket_name
  region      = var.region
  tags = {
    Test        = "true"
    Environment = "Test"
  }
}

variable "bucket_name" {
  description = "Test bucket name."
  type        = string
  default     = "test-chronicle-archive-12345"
}

variable "region" {
  description = "Test region."
  type        = string
  default     = "us-east-1"
}
