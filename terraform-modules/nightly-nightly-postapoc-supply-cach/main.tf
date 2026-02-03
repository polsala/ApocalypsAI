terraform {
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
  region = var.region
}

resource "aws_s3_bucket" "supply_bucket" {
  bucket = var.bucket_name

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id      = "expire-old-supplies"
    enabled = true

    expiration {
      days = 3650
    }

    noncurrent_version_expiration {
      days = 3650
    }
  }

  tags = {
    Purpose = "PostApocalypticSupplyCache"
  }
}

resource "random_pet" "supply_name" {
  length    = 2
  separator = "-"
}

resource "aws_s3_bucket_object" "supply_object" {
  bucket       = aws_s3_bucket.supply_bucket.id
  key          = "supply-cache-${random_pet.supply_name.id}.txt"
  content      = "🧰 Emergency supplies stored here. Stay safe, wanderer!"
  content_type = "text/plain"
}
