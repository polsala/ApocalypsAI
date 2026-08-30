terraform {
  required_version = ">= 1.0"
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

resource "random_pet" "name" {
  length    = 2
  separator = "-"
}

resource "aws_s3_bucket" "safehouse" {
  bucket        = "${var.bucket_prefix}-${random_pet.name.id}"
  force_destroy = false

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
    id      = "expire-old-objects"
    enabled = true

    expiration {
      days = 30
    }

    filter {}
  }

  tags = {
    Name        = "Safehouse S3 Bucket"
    Environment = "production"
  }
}
