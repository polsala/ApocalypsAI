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
  # Dummy configuration for offline validation
  region = "us-east-1"
}

# -------------------------------------------------------------------
# Data source to resolve the IAM role name from the provided ARN
# -------------------------------------------------------------------

data "aws_iam_role" "target" {
  arn = var.allowed_role_arn
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name
  tags   = var.tags
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
    id     = "expire-noncurrent"
    status = "Enabled"

    noncurrent_version_expiration {
      days = 30
    }
  }
}

resource "aws_iam_policy" "safehouse_access" {
  name        = "${var.bucket_name}-access"
  description = "Read/write access to the safehouse S3 bucket"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ],
        Resource = [
          aws_s3_bucket.safehouse.arn,
          "${aws_s3_bucket.safehouse.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach" {
  role       = data.aws_iam_role.target.name
  policy_arn = aws_iam_policy.safehouse_access.arn
}
