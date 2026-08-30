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
  region                      = var.region
  skip_credentials_validation = true
  skip_requesting_account_id  = true
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  lifecycle_rule {
    id      = "expire-old-supplies"
    enabled = true
    expiration {
      days = 30
    }
    filter {}
  }
}

resource "aws_s3_bucket_public_access_block" "safehouse" {
  bucket = aws_s3_bucket.safehouse.id
  block_public_acls   = true
  block_public_policy = true
  ignore_public_acls  = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_object" "supply" {
  count  = var.create_supply ? 1 : 0
  bucket  = aws_s3_bucket.safehouse.id
  key     = "supply-cache.txt"
  content = var.supply_content
}
