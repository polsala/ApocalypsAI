terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
}

provider "aws" {
  region = var.region
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "safehouse" {
  bucket = "${var.bucket_name_prefix}-${random_id.bucket_suffix.hex}"
  force_destroy = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id      = "archive-and-delete"
    enabled = true

    transition {
      days          = 30
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }
}

resource "aws_s3_bucket_public_access_block" "safehouse_block" {
  bucket = aws_s3_bucket.safehouse.id
  block_public_acls   = true
  block_public_policy = true
  ignore_public_acls  = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_object" "starter_supply" {
  bucket  = aws_s3_bucket.safehouse.id
  key     = "starter-supply.txt"
  content = var.supply_content
  acl     = "private"
}
