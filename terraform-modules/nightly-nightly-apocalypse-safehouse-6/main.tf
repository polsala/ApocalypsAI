terraform {
  required_version = ">= 1.0"
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
}

# Optional initial supply object
resource "aws_s3_bucket_object" "welcome" {
  count  = var.initial_supply != "" ? 1 : 0
  bucket  = aws_s3_bucket.safehouse.id
  key     = "welcome.txt"
  content = var.initial_supply
}
