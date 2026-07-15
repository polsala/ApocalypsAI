# Mock rationale: We use a mock provider configuration to ensure tests are deterministic and offline,
# preventing actual cloud resource creation and relying on Terraform's internal plan evaluation.
# The 'terraform test' framework can be configured to use mock providers for more complex scenarios,
# but for simple output assertions, defining a provider block in the test file is sufficient
# to allow the module to be evaluated without live API calls.

provider "aws" {
  region = "us-east-1"
  # Mocking credentials to ensure no real AWS calls are made.
  # In a real 'terraform test' setup, you might use a dedicated mock_provider block
  # or environment variables to control provider behavior.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
  token      = "mock_token"
}

# Test case 1: Default configuration
run "default_config" {
  module {
    source = "../src"

    bucket_name = "test-bunker-vault-default"
    tags = {
      Environment = "Test"
      Project     = "ApocalypsAI"
    }
  }

  assert {
    condition     = module.default_config.bucket_id == "test-bunker-vault-default"
    error_message = "Default bucket ID mismatch"
  }

  assert {
    condition     = module.default_config.bucket_arn == "arn:aws:s3:::test-bunker-vault-default"
    error_message = "Default bucket ARN mismatch"
  }

  assert {
    condition     = module.default_config.bucket_domain_name == "test-bunker-vault-default.s3.us-east-1.amazonaws.com" # Mock rationale: Domain name is predictable based on bucket name and region.
    error_message = "Default bucket domain name mismatch"
  }
}

# Test case 2: With Glacier transition enabled
run "glacier_transition_enabled" {
  module {
    source = "../src"

    bucket_name = "test-bunker-vault-glacier"
    enable_glacier_transition = true
    tags = {
      Environment = "Test"
      Project     = "ApocalypsAI"
    }
  }

  assert {
    condition     = module.glacier_transition_enabled.bucket_id == "test-bunker-vault-glacier"
    error_message = "Glacier bucket ID mismatch"
  }

  assert {
    condition     = module.glacier_transition_enabled.bucket_arn == "arn:aws:s3:::test-bunker-vault-glacier"
    error_message = "Glacier bucket ARN mismatch"
  }

  assert {
    condition     = module.glacier_transition_enabled.bucket_domain_name == "test-bunker-vault-glacier.s3.us-east-1.amazonaws.com" # Mock rationale: Domain name is predictable based on bucket name and region.
    error_message = "Glacier bucket domain name mismatch"
  }
}
