terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
  keepers = {
    # This ensures the random_id changes if the prefix changes, creating a new bucket
    prefix = var.prefix
  }
}

# S3 Data Cache
resource "aws_s3_bucket" "data_cache" {
  count  = var.enable_s3_cache ? 1 : 0
  bucket = "${var.prefix}-data-cache-${random_id.bucket_suffix.hex}"

  tags = {
    Name    = "${var.prefix}-data-cache"
    Purpose = "ApocalypsAI Salvaged Data Cache"
  }
}

resource "aws_s3_bucket_acl" "data_cache_acl" {
  count  = var.enable_s3_cache ? 1 : 0
  bucket = aws_s3_bucket.data_cache[0].id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "data_cache_versioning" {
  count  = var.enable_s3_cache ? 1 : 0
  bucket = aws_s3_bucket.data_cache[0].id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "data_cache_lifecycle" {
  count  = var.enable_s3_cache ? 1 : 0
  bucket = aws_s3_bucket.data_cache[0].id

  rule {
    id     = "cost_saving_transition"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
    transition {
      days          = 90
      storage_class = "GLACIER"
    }
    expiration {
      days = 365
    }
  }
}

# EC2 Communication Relay
data "aws_vpc" "default" {
  count = var.enable_ec2_relay ? 1 : 0
  default = true
}

resource "aws_security_group" "relay_sg" {
  count       = var.enable_ec2_relay ? 1 : 0
  name        = "${var.prefix}-relay-sg"
  description = "Allow SSH and all outbound traffic for ApocalypsAI relay node"
  vpc_id      = data.aws_vpc.default[0].id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # WARNING: Broad access, restrict in production!
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.prefix}-relay-sg"
  }
}

resource "aws_instance" "relay_node" {
  count         = var.enable_ec2_relay ? 1 : 0
  ami           = var.ec2_ami_id
  instance_type = var.ec2_instance_type
  key_name      = var.ec2_key_name
  vpc_security_group_ids = [aws_security_group.relay_sg[0].id]

  tags = {
    Name    = "${var.prefix}-relay-node"
    Purpose = "ApocalypsAI Communication Relay"
  }
}
