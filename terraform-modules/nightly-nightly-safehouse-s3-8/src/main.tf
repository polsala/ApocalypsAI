terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }
}

provider "aws" {
  region = var.region
}

resource "random_pet" "bucket_name" {
  length    = 2
  separator = "-"
  prefix    = var.bucket_prefix
}

resource "aws_s3_bucket" "safehouse" {
  bucket = random_pet.bucket_name.id
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "safehouse_versioning" {
  bucket = aws_s3_bucket.safehouse.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "safehouse_encryption" {
  bucket = aws_s3_bucket.safehouse.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "safehouse_lifecycle" {
  bucket = aws_s3_bucket.safehouse.id

  rule {
    id     = "expire-old-objects"
    status = "Enabled"

    expiration {
      days = var.expiration_days
    }

    filter {}
  }
}
