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
  # In tests we mock credentials; real usage requires proper AWS config.
  region = "us-east-1"
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name

  force_destroy = true
}

resource "aws_s3_bucket_versioning" "safehouse" {
  bucket = aws_s3_bucket.safehouse.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "safehouse" {
  count = var.enable_encryption ? 1 : 0

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
    id     = "glacier-transition"
    status = "Enabled"

    filter {
      prefix = ""
    }

    transition {
      days          = var.transition_days
      storage_class = "GLACIER"
    }

    expiration {
      days = var.expiration_days
    }
  }
}
