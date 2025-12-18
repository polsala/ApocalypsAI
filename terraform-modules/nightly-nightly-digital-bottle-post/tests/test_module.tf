# Mock rationale: This test module calls the main module with mock inputs
# to validate its syntax and ensure it can be planned without errors.
# It does not provision actual resources, making it deterministic and offline.

# Define the AWS provider for the test environment
provider "aws" {
  region = "us-east-1" # Mock region for validation
  # Mock rationale: No actual AWS credentials are needed for `terraform validate` or `terraform plan -no-color`.
  # The provider block is present to satisfy Terraform's configuration requirements for validation.
}

module "digital_bottle_post_public_test" {
  source = "../src" # Path to the module being tested

  bucket_name     = "test-apocalypsai-message-bottle-public-12345" # Mock bucket name
  message_content = "Test message for public validation."
  public_read     = true
}

module "digital_bottle_post_private_test" {
  source = "../src" # Path to the module being tested

  bucket_name     = "test-apocalypsai-message-bottle-private-67890" # Mock bucket name
  message_content = "Secret test message for private validation."
  public_read     = false
}
