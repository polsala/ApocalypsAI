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
  region                      = var.aws_region
  access_key                  = "mock"
  secret_key                  = "mock"
  skip_credentials_validation = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true
  # Endpoint points to a local mock; not needed for validation only
  # endpoints {
  #   s3 = "http://localhost:4566"
  # }
}

resource "aws_s3_bucket" "safehouse" {
  bucket        = "${var.bucket_name}-safehouse"
  tags          = var.tags
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "safehouse" {
  bucket = aws_s3_bucket.safehouse.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "safehouse" {
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
    id     = "expire-old-supplies"
    status = "Enabled"
    expiration {
      days = 30
    }
    filter {}
  }
}

resource "aws_s3_bucket_object" "supplies" {
  bucket  = aws_s3_bucket.safehouse.id
  key     = "supplies.txt"
  content = "Remember: water, canned beans, and hope."
}
