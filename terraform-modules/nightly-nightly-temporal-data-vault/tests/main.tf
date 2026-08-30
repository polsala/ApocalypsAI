provider "aws" {
  region = "us-east-1"
  # Mock rationale: The AWS provider is required for Terraform to parse the HCL, 
  # but no actual AWS credentials or API calls are made during `terraform plan`.
  # The region is a placeholder.
}

module "test_vault" {
  source = "../src"

  bucket_name           = "test-apocalypsai-temporal-vault-12345"
  environment           = "test"
  retention_days_standard = 7
  retention_days_glacier  = 90
}
