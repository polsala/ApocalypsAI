provider "aws" {
  region = "us-east-1" # Mock rationale: Terraform validate/plan can run without actual credentials for syntax checks.
}

resource "random_id" "test_suffix" {
  byte_length = 4 # Shorter for test clarity
}

module "test_whisper_vault" {
  source = "../"

  bucket_name_prefix = "test-whisper-${random_id.test_suffix.hex}-"
  region             = "us-east-1"
  retention_days     = 1 # Short retention for testing ephemerality
}

output "test_bucket_id" {
  value = module.test_whisper_vault.bucket_id
}

output "test_bucket_arn" {
  value = module.test_whisper_vault.bucket_arn
}
