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
  region                       = "us-east-1"
  access_key                   = "mock"
  secret_key                   = "mock"
  skip_credentials_validation  = true
  skip_requesting_account_id   = true
}

resource "aws_s3_bucket" "safehouse" {
  bucket        = var.bucket_name
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
    id     = "expire-old-objects"
    status = "Enabled"
    expiration {
      days = var.expiration_days
    }
    filter {}
  }
}

data "aws_iam_role" "target_role" {
  name = var.iam_role_name
}

resource "aws_iam_policy" "s3_rw_policy" {
  name        = "${var.bucket_name}-rw"
  description = "Read/write access to the safehouse S3 bucket"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "s3:PutObject",
          "s3:GetObject",
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
  role       = data.aws_iam_role.target_role.name
  policy_arn = aws_iam_policy.s3_rw_policy.arn
}
