provider "aws" {
  region = "us-east-1"
  # Mock rationale: For terraform plan, credentials are not strictly needed if
  # the provider configuration is minimal and no actual API calls are made.
  # We are testing the plan generation, not actual deployment.
  # In a real test, one might use dummy credentials or environment variables.
  # For this specific test, we rely on the fact that 'terraform plan'
  # can often proceed without valid credentials if it's only evaluating HCL.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "critter_cache_test" {
  source = "../src"

  bucket_name_prefix = "test-critter-cache-"
  region             = "us-east-1"
  critter_name       = "TestCritter"
  comfort_message    = "Beep boop, you're loved!"
}
