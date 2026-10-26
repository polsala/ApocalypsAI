# Mock rationale: This configuration is for testing the module's syntax and variable handling offline.
# It does not require actual AWS credentials or resource provisioning.
# The provider block is minimal and uses dummy values to satisfy Terraform's parsing requirements
# without attempting to authenticate or connect to a real AWS account during `terraform validate`.
provider "aws" {
  region     = "us-east-1"
  access_key = "mock_access_key" # Mock rationale: Dummy value for offline validation.
  secret_key = "mock_secret_key" # Mock rationale: Dummy value for offline validation.
  token      = "mock_token"      # Mock rationale: Dummy value for offline validation.
}

# Mock rationale: The TLS provider is used to generate an SSH key pair.
# For offline testing, it only needs to be declared; no actual key material is persisted or used beyond validation.
provider "tls" {}

module "test_shelter" {
  source = "../src"

  name_prefix = "test-shelter-123"
  region      = "us-east-1"
  ami_id      = "ami-053b0d53c279acc90" # Mock rationale: A valid AMI ID for syntax check, not actually looked up.
  instance_type = "t2.micro"
  create_key_pair = true
  tags = {
    Environment = "Test"
    Project     = "ApocalypsAI"
  }
}

module "test_shelter_existing_key" {
  source = "../src"

  name_prefix = "test-shelter-existing-key"
  region      = "us-east-1"
  ami_id      = "ami-053b0d53c279acc90" # Mock rationale: A valid AMI ID for syntax check, not actually looked up.
  instance_type = "t2.micro"
  create_key_pair = false
  ssh_key_name = "my-existing-ssh-key" # Mock rationale: Assumes an existing key for validation.
  tags = {
    Environment = "Test"
    Project     = "ApocalypsAI"
  }
}
