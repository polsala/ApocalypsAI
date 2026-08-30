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
  region = var.aws_region
}

resource "random_pet" "suffix" {
  count  = var.enable_random_suffix ? 1 : 0
  length = 2
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.enable_random_suffix ? "${var.bucket_name}-${random_pet.suffix[0].id}" : var.bucket_name

  force_destroy = true

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
    id      = "expire-old-versions"
    enabled = true

    noncurrent_version_expiration {
      days = 30
    }
  }

  tags = {
    Purpose = "Apocalypse Safehouse"
  }
}

output "bucket_id" {
  value = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  value = aws_s3_bucket.safehouse.arn
}

output "bucket_name" {
  value = aws_s3_bucket.safehouse.bucket
}
