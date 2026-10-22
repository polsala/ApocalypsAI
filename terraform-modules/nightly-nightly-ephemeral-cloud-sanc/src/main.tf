terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

resource "aws_vpc" "sanctuary_vpc" {
  cidr_block = var.vpc_cidr_block
  tags = {
    Name        = "${var.project_name}-sanctuary-vpc"
    Environment = "ephemeral"
  }
}

resource "aws_subnet" "sanctuary_subnet" {
  vpc_id     = aws_vpc.sanctuary_vpc.id
  cidr_block = var.subnet_cidr_block
  # Simple AZ selection for basic functionality, can be made more robust
  availability_zone = var.aws_region == "us-east-1" ? "us-east-1a" : "${var.aws_region}a"
  tags = {
    Name        = "${var.project_name}-sanctuary-subnet"
    Environment = "ephemeral"
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "sanctuary_bucket" {
  bucket = "${var.project_name}-ephemeral-sanctuary-${random_id.bucket_suffix.hex}"
  acl    = "private"
  tags = {
    Name        = "${var.project_name}-sanctuary-bucket"
    Environment = "ephemeral"
  }
}
