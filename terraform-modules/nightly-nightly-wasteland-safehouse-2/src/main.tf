terraform {
  required_version = ">= 1.0.0"
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

  tags = {
    Purpose = "PostApocalypticSafehouse"
  }
}

resource "aws_s3_bucket_object" "supply_cache" {
  bucket       = aws_s3_bucket.safehouse.id
  key          = "supply-cache.txt"
  content      = "🧪 Emergency supplies: water, canned beans, and a dash of hope."
  content_type = "text/plain"
}
