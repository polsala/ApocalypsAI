# Mock rationale: This configuration is used solely for offline validation
# of the module's syntax and structure using 'terraform validate' and 'terraform fmt'.
# It does not require AWS credentials or actual resource deployment.

provider "aws" {
  region = "us-east-1" # Placeholder region for validation
}

module "test_echo_chamber_bucket" {
  source = "../src" # Path to the module being tested

  bucket_name = "test-echo-chamber-bucket-12345"
  region      = "us-east-1"
  tags = {
    Test        = "True"
    Environment = "Test"
  }
}
