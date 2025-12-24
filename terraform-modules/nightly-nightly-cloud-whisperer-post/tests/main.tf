provider "aws" {
  region = "us-east-1" # Mock rationale: Region is needed for provider config but not for plan output checks.
  # Mock rationale: No actual AWS credentials are used for `terraform plan`. These are dummy values.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
  token      = "mock_token"
}

module "test_postbox" {
  source = "../src"

  bucket_name_prefix = "test-whisper-postbox"
  sns_topic_name     = "test-whisper-channel"
  notification_filter_prefix = "inbox/"
  tags = {
    Environment = "Test"
    Project     = "ApocalypsAI"
  }
}
