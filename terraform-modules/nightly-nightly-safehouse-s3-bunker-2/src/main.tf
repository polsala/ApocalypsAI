terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

variable "bucket_prefix" {
  description = "Prefix for the bucket name"
  type        = string
  default     = "safehouse"
}

resource "random_pet" "name" {
  length    = 2
  separator = "-"
}

resource "aws_s3_bucket" "bunker" {
  bucket        = "${var.bucket_prefix}-${random_pet.name.id}"
  force_destroy = true
  tags = {
    Purpose = "Apocalypse Safehouse"
  }
}

resource "aws_s3_bucket_versioning" "bunker_versioning" {
  bucket = aws_s3_bucket.bunker.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "bunker_encryption" {
  bucket = aws_s3_bucket.bunker.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "bunker_lifecycle" {
  bucket = aws_s3_bucket.bunker.id
  rule {
    id     = "expire-old-objects"
    status = "Enabled"
    expiration {
      days = 30
    }
    filter {}
  }
}

output "bucket_name" {
  description = "The name of the created S3 bucket"
  value       = aws_s3_bucket.bunker.bucket
}
