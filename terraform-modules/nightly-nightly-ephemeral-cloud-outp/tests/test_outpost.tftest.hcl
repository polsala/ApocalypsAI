# Mock rationale:
# The 'mock_provider' blocks simulate the AWS and TLS provider behavior,
# allowing the Terraform tests to run deterministically and offline without
# requiring actual AWS credentials or making real API calls. This ensures
# that the module's HCL syntax, variable handling, resource declarations,
# and output generation are correct.

provider "aws" {
  region = "us-east-1"
  # Mocking the AWS provider to prevent actual cloud resource creation
  # and allow offline, deterministic testing.
  # Mock rationale: Simulates AWS API responses for resource creation and data lookups.
  mock_provider "aws" {
    data "aws_vpc" "default" {
      id      = "vpc-mockdefault"
      default = true
    }
    resource "aws_key_pair" "ephemeral_key" {
      key_name   = "test-key"
      public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD3N..." # Mock public key
      id         = "key-mockid"
    }
    resource "aws_security_group" "ephemeral_sg" {
      id          = "sg-mockid"
      name        = "test-outpost-sg"
      vpc_id      = "vpc-mockdefault"
      description = "Security group for test-outpost"
      ingress = [
        {
          from_port   = 22
          to_port     = 22
          protocol    = "tcp"
          cidr_blocks = ["0.0.0.0/0"]
        },
        {
          from_port   = 80
          to_port     = 80
          protocol    = "tcp"
          cidr_blocks = ["0.0.0.0/0"]
        }
      ]
      egress = [
        {
          from_port   = 0
          to_port     = 0
          protocol    = "-1"
          cidr_blocks = ["0.0.0.0/0"]
        }
      ]
    }
    resource "aws_instance" "ephemeral_outpost" {
      id                     = "i-mockinstanceid"
      ami                    = "ami-mockami"
      instance_type          = "t2.micro"
      key_name               = "test-key"
      vpc_security_group_ids = ["sg-mockid"]
      public_ip              = "192.0.2.1" # Mock IP
      tags = {
        Name = "test-outpost"
      }
    }
  }
}

provider "tls" {
  # Mocking the TLS provider to generate a dummy private key for testing.
  # Mock rationale: Simulates TLS key generation without actual cryptographic operations.
  mock_provider "tls" {
    resource "tls_private_key" "ephemeral_key" {
      algorithm          = "RSA"
      rsa_bits           = 2048
      private_key_pem    = "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAs..." # Mock private key
      public_key_openssh = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD3N..." # Mock public key
    }
  }
}

run "plan_and_apply" {
  module {
    source = "./src"
    # Provide required variables for the module
    ami_id        = "ami-mockami"
    instance_name = "test-outpost"
    key_name      = "test-key"
    ingress_ports = [22, 80]
    region        = "us-east-1"
  }

  command = plan
  expect_changes = true # Expect resources to be created

  # Verify that specific resources are planned for creation
  check {
    values = module.ephemeral_outpost
    assert {
      condition     = module.ephemeral_outpost.instance_id == "i-mockinstanceid"
      error_message = "Expected instance_id to be 'i-mockinstanceid'"
    }
    assert {
      condition     = module.ephemeral_outpost.public_ip == "192.0.2.1"
      error_message = "Expected public_ip to be '192.0.2.1'"
    }
    assert {
      condition     = module.ephemeral_outpost.security_group_id == "sg-mockid"
      error_message = "Expected security_group_id to be 'sg-mockid'"
    }
    assert {
      condition     = length(module.ephemeral_outpost.private_key_pem) > 0
      error_message = "Expected private_key_pem to be non-empty"
    }
  }
}

run "destroy" {
  module {
    source = "./src"
    ami_id        = "ami-mockami"
    instance_name = "test-outpost"
    key_name      = "test-key"
    ingress_ports = [22, 80]
    region        = "us-east-1"
  }

  command = destroy
  expect_changes = true # Expect resources to be destroyed
}
