terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
}

provider "aws" {
  region                      = var.region
  skip_credentials_validation = true
  skip_get_ec2_platforms      = true
  skip_metadata_api_check     = true
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name
  force_destroy = true
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
    id     = "expire-old-objects"
    status = "Enabled"
    expiration {
      days = 30
    }
  }
}

resource "aws_iam_policy" "read_only_policy" {
  name        = "${var.bucket_name}-read-only"
  description = "Read‑only access to the safehouse bucket"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect   = "Allow",
      Action   = ["s3:GetObject", "s3:ListBucket"],
      Resource = [
        aws_s3_bucket.safehouse.arn,
        "${aws_s3_bucket.safehouse.arn}/*"
      ]
    }]
  })
}
