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
  # Configuration is expected to be provided by the caller (e.g., via env vars)
}

resource "aws_s3_bucket" "supply_cache" {
  bucket = var.bucket_name

  tags = {
    "apocalypse:ready" = random_pet.emoji.id
  }
}

resource "aws_s3_bucket_versioning" "supply_cache_versioning" {
  bucket = aws_s3_bucket.supply_cache.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "supply_cache_encryption" {
  bucket = aws_s3_bucket.supply_cache.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "supply_cache_lifecycle" {
  bucket = aws_s3_bucket.supply_cache.id

  rule {
    id     = "expire-old-supplies"
    status = "Enabled"

    expiration {
      days = 30
    }

    filter {}
  }
}

resource "random_pet" "emoji" {
  length = 1
}
