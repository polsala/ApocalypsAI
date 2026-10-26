# Mock rationale: This configuration is used for testing the module's syntax and planned output
# without actually provisioning AWS resources. It acts as a mock deployment.

provider "aws" {
  region = "us-east-1"
  # Mock rationale: Using a dummy access key and secret key to allow terraform init/plan
  # to proceed without valid AWS credentials, as we are not performing an apply.
  access_key = "mock_access_key" 
  secret_key = "mock_secret_key"
  token      = "mock_session_token" # For temporary credentials
}

module "test_echo_chamber_vault" {
  source = "../src" # Path to the module being tested
  
  bucket_name_prefix = "test-apocalypsai-echo"
  expiration_days    = 5
  tags = {
    TestEnv = "True"
  }
}

output "test_bucket_id" {
  value = module.test_echo_chamber_vault.bucket_id
}

output "test_bucket_arn" {
  value = module.test_echo_chamber_vault.bucket_arn
}
