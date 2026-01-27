# Mock rationale: For offline testing, we need to provide dummy IDs for VPC and Subnet.
# These values are not actually used to provision resources during `terraform plan`,
# but satisfy the module's input requirements for validation.
resource "aws_vpc" "mock_vpc" {
  # This resource is purely for satisfying the module's input requirements during testing.
  # It will not be created during `terraform plan` if the module is run in isolation
  # and only `terraform plan` is executed.
  # Its purpose is to provide a valid-looking ID for the `vpc_id` input.
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "mock-vpc-for-test"
  }
}

resource "aws_subnet" "mock_subnet" {
  # Similar to mock_vpc, this provides a valid-looking ID for `subnet_id`.
  vpc_id     = aws_vpc.mock_vpc.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "us-east-1a" # Dummy AZ
  tags = {
    Name = "mock-subnet-for-test"
  }
}

module "chronos_chronometer_test" {
  source = "../src" # Reference the module under test

  aws_region    = "us-east-1"
  vpc_id        = aws_vpc.mock_vpc.id
  subnet_id     = aws_subnet.mock_subnet.id
  instance_type = "t2.micro"
  allowed_cidrs = ["0.0.0.0/0"] # Allow all for testing purposes
  key_name      = null # No key needed for plan test
  tags = {
    Environment = "Test"
    Purpose     = "ChronosChronometerTest"
  }
}
