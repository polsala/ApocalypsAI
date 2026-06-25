module "test_chronos_cache" {
  source = "../src"

  bucket_name = "apocalypsai-test-chronos-cache-12345" # Unique name for testing
  bucket_acl  = "private"
  tags = {
    Environment = "Test"
    Project     = "ApocalypsAI"
  }
}
