provider "aws" {
  region = "us-east-1" # Mock rationale: Required by Terraform for provider configuration, but no actual API calls are made during `terraform validate` or `terraform plan -destroy`.
}

module "test_scavenger_cache" {
  source = "../src"

  bucket_name = "test-apocalypsai-scavenger-cache-12345"
  environment = "test"
  tags = {
    Project = "ApocalypsAI"
    Purpose = "TestCache"
  }
  glacier_transition_days = 7
  # access_logging_bucket_name = ["test-log-bucket-12345"] # Mock rationale: Can be uncommented for a more complete test, but not strictly necessary for offline syntax validation.
}
