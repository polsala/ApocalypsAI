module "chronos_cache_test" {
  source = "../src" # Path to the module being tested

  bucket_name = "apocalypsai-chronos-cache-test-12345"
  tags = {
    Environment = "Test"
    Project     = "ApocalypsAI"
  }
}

output "test_bucket_id" {
  value = module.chronos_cache_test.bucket_id
}

output "test_bucket_arn" {
  value = module.chronos_cache_test.bucket_arn
}
