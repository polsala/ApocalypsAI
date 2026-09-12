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
  region = "us-east-1"
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name
  tags   = var.tags

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id      = "expire-old-objects"
    enabled = true

    expiration {
      days = 365
    }

    noncurrent_version_expiration {
      days = 30
    }
  }
}

resource "aws_iam_policy" "safehouse_readonly" {
  name        = "${var.bucket_name}-readonly"
  description = "Read‑only access to the safehouse bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:ListBucket"]
        Resource = [
          aws_s3_bucket.safehouse.arn,
          "${aws_s3_bucket.safehouse.arn}/*"
        ]
      }
    ]
  })
}
