# Mock rationale: This test configuration is designed to validate the module's syntax
# and variable definitions without requiring actual AWS credentials or resource deployment.
# It uses a null provider to satisfy Terraform's requirement for a provider,
# but no actual resources are created. The primary test is `terraform validate`.

provider "aws" {
  region = "us-east-1"
  # Mock rationale: Using a dummy access key and secret key to allow `terraform init`
  # and `terraform validate` to proceed without real credentials.
  # These are not used for actual resource provisioning in this test.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "test_observatory" {
  source = "../src"

  bucket_name_prefix = "test-celestial-anomalies"
  tags = {
    Environment = "Test"
    Project     = "ApocalypsAI"
  }
  enable_glacier_archive  = true
  glacier_archive_days    = 30
  glacier_expiration_days = 180
}

output "test_bucket_id" {
  value = module.test_observatory.bucket_id
}

output "test_bucket_arn" {
  value = module.test_observatory.bucket_arn
}
