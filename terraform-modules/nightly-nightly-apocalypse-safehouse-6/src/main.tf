terraform {
  required_version = ">= 1.3.0"
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
  # Dummy credentials for offline testing
  access_key = "FAKEACCESSKEY"
  secret_key = "FAKESECRETKEY"
  region     = "us-east-1"
  skip_credentials_validation = true
  skip_requesting_account_id   = true
  s3_use_path_style           = true
  endpoints {
    s3 = "http://localhost:4566" # Mock S3 endpoint (e.g., LocalStack) – not used in offline test
  }
}

resource "random_pet" "suffix" {
  length = 2
}

resource "aws_s3_bucket" "safehouse" {
  bucket        = "${var.bucket_name_prefix}-${random_pet.suffix.id}"
  force_destroy = true

  tags = var.tags
}

resource "aws_s3_bucket_versioning" "safehouse_versioning" {
  bucket = aws_s3_bucket.safehouse.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "safehouse_enc" {
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
    id     = "expire-old-versions"
    status = "Enabled"

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}
