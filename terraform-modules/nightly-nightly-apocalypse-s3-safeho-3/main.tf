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
  # In test environments, use dummy credentials and region
  access_key = "test"
  secret_key = "test"
  region     = "us-east-1"
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
  }

  tags = {
    Purpose = "Apocalyptic Safehouse"
  }
}

resource "aws_s3_bucket_object" "supply_cache" {
  bucket  = aws_s3_bucket.safehouse.id
  key     = "supply-cache.txt"
  content = "Placeholder supplies for the end times."
}
