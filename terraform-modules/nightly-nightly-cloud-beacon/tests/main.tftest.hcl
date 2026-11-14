# Mock rationale: These mocks simulate AWS resource creation and attribute values
# without actually provisioning any cloud infrastructure, ensuring tests are
# deterministic, fast, and offline.

provider "aws" {
  region = "us-east-1"
  # Mock rationale: The provider block is mocked to prevent actual AWS API calls.
  # All resource interactions are intercepted and simulated by the mock blocks below.
  mock_account_id = "123456789012"
  mock_caller_arn = "arn:aws:iam::123456789012:user/test"
  mock_partition  = "aws"
}

provider "random" {
  # Mock rationale: The random provider is mocked to ensure the bucket suffix is
  # deterministic, preventing test failures due to random values.
  mock_values = {
    string = {
      result = "mockedsuffix"
    }
  }
}

run "default_beacon_deployment" {
  variables {
    region         = "us-east-1"
    instance_type  = "t2.micro"
    beacon_message = "Test message for the beacon."
    key_name       = "" # No key for default test
  }

  # Mock rationale: These mock blocks simulate the creation of AWS resources
  # and define their expected attributes, allowing the Terraform module to be
  # tested without real cloud interaction.
  mock_resource "aws_vpc" "beacon_vpc" {
    id         = "vpc-mockvpcid"
    cidr_block = "10.0.0.0/16"
  }
  mock_resource "aws_internet_gateway" "beacon_igw" {
    id     = "igw-mockigwid"
    vpc_id = "vpc-mockvpcid"
  }
  mock_resource "aws_subnet" "beacon_subnet" {
    id                      = "subnet-mocksubnetid"
    vpc_id                  = "vpc-mockvpcid"
    cidr_block              = "10.0.1.0/24"
    map_public_ip_on_launch = true
  }
  mock_resource "aws_route_table" "beacon_rt" {
    id     = "rtb-mockrtbid"
    vpc_id = "vpc-mockvpcid"
  }
  mock_resource "aws_route_table_association" "beacon_rta" {
    id             = "rtbassoc-mockrtaid"
    subnet_id      = "subnet-mocksubnetid"
    route_table_id = "rtb-mockrtbid"
  }
  mock_resource "aws_security_group" "beacon_sg" {
    id     = "sg-mocksgid"
    vpc_id = "vpc-mockvpcid"
    ingress {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
    ingress {
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
    ingress {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
  mock_data "aws_ami" "ubuntu" {
    id = "ami-mockamiid"
  }
  mock_resource "aws_instance" "beacon_server" {
    id                          = "i-mockinstanceid"
    ami                         = "ami-mockamiid"
    instance_type               = "t2.micro"
    subnet_id                   = "subnet-mocksubnetid"
    vpc_security_group_ids      = ["sg-mocksgid"]
    associate_public_ip_address = true
    user_data                   = "mocked_user_data_script" # Content is not directly asserted in mock
  }
  mock_resource "aws_eip" "beacon_eip" {
    id        = "eipalloc-mockeipallocid"
    public_ip = "192.0.2.123" # Example IP
    instance  = "i-mockinstanceid"
    vpc       = true
  }
  mock_resource "aws_s3_bucket" "beacon_message_archive" {
    id     = "apocalypsai-beacon-archive-mockedsuffix"
    bucket = "apocalypsai-beacon-archive-mockedsuffix"
    acl    = "private"
  }

  assert {
    # Mock rationale: Assertions verify that the module's outputs match the
    # expected values based on the mocked resource attributes.
    condition     = output.beacon_public_ip == "192.0.2.123"
    error_message = "Beacon public IP output is incorrect."
  }
  assert {
    condition     = output.beacon_url == "http://192.0.2.123"
    error_message = "Beacon URL output is incorrect."
  }
  assert {
    condition     = output.s3_bucket_name == "apocalypsai-beacon-archive-mockedsuffix"
    error_message = "S3 bucket name output is incorrect."
  }
}

run "custom_instance_type" {
  variables {
    region         = "us-east-1"
    instance_type  = "t3.small" # Test with a different instance type
    beacon_message = "Another test message."
    key_name       = "my-ssh-key"
  }

  # Mock rationale: Re-mocking resources to simulate different input variables.
  mock_resource "aws_instance" "beacon_server" {
    id                          = "i-mockinstanceid-t3small"
    ami                         = "ami-mockamiid"
    instance_type               = "t3.small" # Expected change
    subnet_id                   = "subnet-mocksubnetid"
    vpc_security_group_ids      = ["sg-mocksgid"]
    associate_public_ip_address = true
    key_name                    = "my-ssh-key" # Expected change
  }
  mock_resource "aws_eip" "beacon_eip" {
    id        = "eipalloc-mockeipallocid-t3small"
    public_ip = "192.0.2.124" # Different IP for this run
    instance  = "i-mockinstanceid-t3small"
    vpc       = true
  }

  assert {
    condition     = output.beacon_public_ip == "192.0.2.124"
    error_message = "Custom instance type public IP output is incorrect."
  }
  assert {
    condition     = output.beacon_url == "http://192.0.2.124"
    error_message = "Custom instance type URL output is incorrect."
  }
}
