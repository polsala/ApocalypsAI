# This is a test configuration to instantiate the module.
# It uses dummy values for testing purposes.

module "test_chrono_cache" {
  source = "../src" # Path to the module under test

  bucket_name_prefix = "test-ephemeral-data"
  expiration_days    = 5
  region             = "us-east-1" # Dummy region for plan validation
}

output "test_bucket_id" {
  value = module.test_chrono_cache.bucket_id
}

output "test_bucket_arn" {
  value = module.test_chrono_cache.bucket_arn
}
