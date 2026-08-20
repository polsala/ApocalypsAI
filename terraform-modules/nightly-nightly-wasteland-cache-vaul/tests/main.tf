provider "aws" {
  region = "us-east-1" # Mock region, not actually used for apply
  # Mock rationale: No actual AWS credentials are required for `terraform plan -json`.
  # The provider block is necessary for Terraform to parse the configuration,
  # but the credentials will not be used for the plan operation itself.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "wasteland_cache" {
  source = "../src"

  bucket_name = "test-wasteland-cache-vault-12345"
  tags = {
    Environment = "Test"
    Project     = "ApocalypsAI"
  }
  retention_days_standard_to_ia    = 15
  retention_days_ia_to_glacier     = 60
  retention_days_glacier_to_delete = 180
}
