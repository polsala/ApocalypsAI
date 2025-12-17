provider "aws" {
  region = "us-east-1" # Mock region for validation
  # Mock rationale: Provider block is needed for Terraform to understand resource types,
  # but actual credentials are not required for `terraform validate` or `terraform plan -destroy`.
  # We use a placeholder region.
}

module "test_chrono_vault" {
  source = "../src"

  bucket_name = "apocalypsai-test-chrono-vault-12345" # Unique name for testing
  encryption_algorithm = "AES256"
  noncurrent_version_transition_days = 7
  noncurrent_version_expiration_days = 90
  enable_static_website = true
  website_index_document = "manifest.html"
  tags = {
    Environment = "Test"
    Project     = "ApocalypsAI"
  }
}

module "test_chrono_vault_kms" {
  source = "../src"

  bucket_name = "apocalypsai-test-chrono-vault-kms-67890"
  encryption_algorithm = "aws:kms"
  kms_key_arn = "arn:aws:kms:us-east-1:123456789012:key/mock-kms-key-id" # Mock ARN
  # Mock rationale: A valid-looking ARN is needed for Terraform's type validation,
  # but this key will not be used or checked against a real AWS account during offline tests.
  enable_static_website = false
  attach_policy = false
}
