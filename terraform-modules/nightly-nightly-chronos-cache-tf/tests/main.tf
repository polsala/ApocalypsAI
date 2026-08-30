# Mock rationale: This test configuration uses a minimal AWS provider block
# to allow 'terraform validate' and 'terraform plan' to run deterministically offline.
# It does NOT provision actual cloud resources. The provider configuration
# is set up to skip credential validation and metadata checks, making it suitable
# for syntax and plan generation checks without live AWS interaction.
provider "aws" {
  region                      = "us-east-1"
  access_key                  = "mock_access_key" # Mock rationale: Dummy key for offline validation.
  secret_key                  = "mock_secret_key" # Mock rationale: Dummy secret for offline validation.
  skip_credentials_validation = true              # Mock rationale: Avoids needing real credentials.
  skip_requesting_account_id  = true              # Mock rationale: Avoids needing real credentials.
  skip_metadata_api_check     = true              # Mock rationale: Avoids needing real credentials.
  s3_use_path_style           = true              # Mock rationale: For consistent local testing behavior.
}

module "chronos_cache_test" {
  source = "../src"

  bucket_name_prefix = "test-chronos-cache"
  expiration_days    = 3
  tags = {
    Environment = "Test"
    Project     = "ApocalypsAI"
  }
}

# Mock rationale: A null_resource to ensure Terraform has something to "plan"
# and to demonstrate that the module can be instantiated and its outputs accessed.
resource "null_resource" "test_trigger" {
  triggers = {
    bucket_id = module.chronos_cache_test.bucket_id
  }
  # Mock rationale: This local-exec is purely for demonstrating a successful plan
  # without actual side effects. It confirms the module outputs are accessible.
  provisioner "local-exec" {
    command = "echo 'Chronos Cache ID: ${self.triggers.bucket_id}'"
  }
}
