provider "aws" {
  region = "us-east-1" # Mock rationale: Required by Terraform for validation, but no actual AWS calls are made during `terraform validate`.
  # access_key = "mock_access_key" # Mock rationale: Not needed for `terraform validate` or `fmt --check`.
  # secret_key = "mock_secret_key" # Mock rationale: Not needed for `terraform validate` or `fmt --check`.
}

module "test_wasteland_cache" {
  source = "../src"

  bucket_name                = "test-apocalypsai-wasteland-cache-12345"
  region                     = "us-east-1"
  enable_versioning          = true
  enable_encryption          = true
  enable_public_access_block = true
  tags = {
    Environment = "Test"
    Project     = "ApocalypsAI"
  }
}

output "test_bucket_id" {
  value = module.test_wasteland_cache.s3_bucket_id
}
