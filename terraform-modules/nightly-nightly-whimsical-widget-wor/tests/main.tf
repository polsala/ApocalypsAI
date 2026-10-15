provider "aws" {
  region = "us-east-1"
  # Mock rationale: Using a dummy access key and secret for offline testing.
  # Terraform validate/plan does not require valid credentials for syntax checks.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "test_workshop" {
  source = "../src"

  project_name  = "test-widget"
  aws_region    = "us-east-1"
  instance_type = "t2.micro"
  ami_id        = "ami-0abcdef1234567890" # Mock rationale: Placeholder AMI for testing.
  ssh_key_name  = null # No SSH key needed for basic validation
}

output "test_vpc_id" {
  value = module.test_workshop.vpc_id
}

output "test_public_ip" {
  value = module.test_workshop.public_ip
}

output "test_security_group_id" {
  value = module.test_workshop.security_group_id
}
