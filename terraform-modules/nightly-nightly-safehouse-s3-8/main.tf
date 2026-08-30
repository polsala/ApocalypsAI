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

provider "aws" {
  # Configuration is expected to be provided via environment variables
  # e.g., AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
}

resource "random_pet" "bucket_suffix" {
  length    = 2
  separator = "-"
  keepers = {
    bucket_name = var.bucket_name
  }
}

locals {
  final_bucket_name = var.bucket_name != null ? var.bucket_name : "safehouse-${random_pet.bucket_suffix.id}"
}

resource "aws_s3_bucket" "safehouse" {
  bucket = local.final_bucket_name

  tags = {
    Name        = "Safehouse Bucket"
    Environment = "post-apocalyptic"
  }
}

resource "aws_s3_bucket_versioning" "safehouse_versioning" {
  bucket = aws_s3_bucket.safehouse.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "safehouse_lifecycle" {
  bucket = aws_s3_bucket.safehouse.id

  rule {
    id     = "expire-noncurrent"
    status = "Enabled"

    noncurrent_version_expiration {
      days = 365
    }
  }
}
