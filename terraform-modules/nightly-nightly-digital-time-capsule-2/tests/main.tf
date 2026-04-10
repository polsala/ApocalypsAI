provider "aws" {
  region = "us-east-1"
  # Mock rationale: In a real test, this would point to a mock AWS endpoint or use credentials.
  # For offline validation, the provider block is needed for syntax, but no actual API calls are made.
}

module "test_time_capsule" {
  source = "../src"

  bucket_name_prefix      = "test-capsule-"
  enable_versioning       = true
  glacier_transition_days = 30
  expiration_days         = 90
}

output "test_bucket_id" {
  value = module.test_time_capsule.bucket_id
}
