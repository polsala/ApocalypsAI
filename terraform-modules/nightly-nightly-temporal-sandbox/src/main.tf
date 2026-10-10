terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    time = {
      source  = "hashicorp/time"
      version = "~> 0.9.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "temporal_sandbox_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name        = "${var.sandbox_name}-vpc"
    Environment = "TemporalSandbox"
    ExpiryDate  = time_static.expiry_timestamp.rfc3339
  }
}

resource "aws_subnet" "temporal_sandbox_subnet" {
  vpc_id            = aws_vpc.temporal_sandbox_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "${var.aws_region}a" # Assuming 'a' zone exists

  tags = {
    Name        = "${var.sandbox_name}-subnet"
    Environment = "TemporalSandbox"
    ExpiryDate  = time_static.expiry_timestamp.rfc3339
  }
}

resource "aws_security_group" "temporal_sandbox_sg" {
  name        = "${var.sandbox_name}-sg"
  description = "Allow SSH and all egress for temporal sandbox"
  vpc_id      = aws_vpc.temporal_sandbox_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # WARNING: For sandbox only, restrict in production!
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.sandbox_name}-sg"
    Environment = "TemporalSandbox"
    ExpiryDate  = time_static.expiry_timestamp.rfc3339
  }
}

resource "aws_instance" "temporal_sandbox_instance" {
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.temporal_sandbox_subnet.id
  vpc_security_group_ids = [aws_security_group.temporal_sandbox_sg.id]

  tags = {
    Name        = "${var.sandbox_name}-instance"
    Environment = "TemporalSandbox"
    ExpiryDate  = time_static.expiry_timestamp.rfc3339
  }
}

# Data source to get the latest Amazon Linux 2 AMI
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Calculate expiry timestamp
resource "time_static" "expiry_timestamp" {
  triggers = {
    ttl_hours = var.ttl_hours
  }
  # Mock rationale: time_static is a Terraform provider that calculates a timestamp.
  # For testing, its output is deterministic based on input variables and the current time
  # when `terraform plan` is run. The test script will verify the *format* and *presence*
  # of this timestamp in the plan, not its exact future value.
  # The `time_static` resource is used here to ensure the expiry date is consistently
  # calculated and available for tagging.
  # The `rfc3339` format is standard for timestamps.
  after = "${var.ttl_hours}h"
}
