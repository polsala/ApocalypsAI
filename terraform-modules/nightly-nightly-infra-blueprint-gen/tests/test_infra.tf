# Mock rationale: This test file uses a mock AMI ID and bucket name to ensure the Terraform configuration is syntactically correct and can be planned without external dependencies.

provider "aws" {
  region = "us-east-1"
  # Mock credentials for testing purposes
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "test_web_server_infra" {
  source = ".."

  instance_type = "t2.micro"
  ami_id        = "ami-0abcdef1234567890" # Mock AMI ID
  bucket_name   = "my-test-unique-bucket-12345"
}

output "test_instance_id" {
  value = module.test_web_server_infra.instance_id
}

output "test_security_group_id" {
  value = module.test_web_server_infra.security_group_id
}

output "test_bucket_name" {
  value = module.test_web_server_infra.bucket_name
}
