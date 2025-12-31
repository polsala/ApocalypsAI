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
  # In tests we rely on the default (mock) provider configuration.
  # Users should configure their credentials as usual.
  region = var.aws_region
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name
  tags   = var.tags
}

resource "aws_s3_bucket_versioning" "safehouse" {
  bucket = aws_s3_bucket.safehouse.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "safehouse" {
  bucket = aws_s3_bucket.safehouse.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "safehouse" {
  bucket = aws_s3_bucket.safehouse.id
  rule {
    id     = "expire‑old‑supplies"
    status = "Enabled"
    expiration {
      days = 30
    }
    filter {}
  }
}

resource "aws_s3_object" "supply_cache" {
  count  = var.create_supply_file ? 1 : 0
  bucket = aws_s3_bucket.safehouse.id
  key    = "supply‑cache.txt"
  content = "Placeholder for your apocalypse supplies. Update this file with actual inventory."
  server_side_encryption = "AES256"
}
