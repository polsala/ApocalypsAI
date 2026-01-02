provider "aws" {
  region = "us-east-1"
  # Mock rationale: For `terraform plan` to succeed without actual AWS credentials,
  # we need a provider block. The `plan` command doesn't interact with the actual API
  # if only local resources or module outputs are being checked. The values here are placeholders.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "test_critter_zone" {
  source = "../" # Refers to the parent directory where the module is defined

  ami_id        = "ami-test-12345"
  instance_type = "t3.nano"
  key_pair_name = "test-key-pair"
  vpc_id        = "vpc-test-abcdef"
  critter_name  = "TestCritter"
}

output "test_instance_public_ip" {
  value = module.test_critter_zone.instance_public_ip
}

output "test_instance_id" {
  value = module.test_critter_zone.instance_id
}

output "test_security_group_id" {
  value = module.test_critter_zone.security_group_id
}
