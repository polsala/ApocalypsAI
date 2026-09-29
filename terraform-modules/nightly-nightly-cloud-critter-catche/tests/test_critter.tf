# This file is used by the test script to instantiate the module
# and run `terraform plan` against it for validation.

provider "aws" {
  region = "us-east-1"
  # Mock rationale: For offline `terraform plan` and `validate`,
  # no actual AWS credentials are required. The provider block is
  # necessary for Terraform to understand the resource types.
  # Access key and secret key are intentionally omitted as they are not
  # needed for plan/validate and would violate "no secrets in logs".
  access_key = "mock_access_key" # Mock rationale: Dummy value for provider block.
  secret_key = "mock_secret_key" # Mock rationale: Dummy value for provider block.
}

module "test_critter_catcher" {
  source = "../src" # Relative path to the module under test

  critter_name      = "test-critter-alpha"
  region            = "us-east-1"
  ami_id            = "ami-053b0d534c279acc9" # Example Amazon Linux 2 AMI in us-east-1
  instance_type     = "t2.micro"
  lifespan_minutes  = 5
  vpc_security_group_ids = []
  subnet_id              = null
}

module "test_critter_catcher_custom" {
  source = "../src" # Relative path to the module under test

  critter_name      = "test-critter-beta"
  region            = "eu-west-1"
  ami_id            = "ami-0a00c735b5465718a" # Example Amazon Linux 2 AMI in eu-west-1
  instance_type     = "t3.small"
  lifespan_minutes  = 15
  vpc_security_group_ids = ["sg-mock1", "sg-mock2"] # Mock rationale: Dummy security group IDs for testing list input.
  subnet_id              = "subnet-mock1" # Mock rationale: Dummy subnet ID for testing string input.
}
