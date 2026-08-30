terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name

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
    id      = "glacier-transition"
    enabled = true

    noncurrent_version_transition {
      days          = 30
      storage_class = "GLACIER"
    }
  }

  tags = {
    Purpose = "Apocalypse Safehouse"
  }
}

resource "aws_iam_policy" "safehouse_access" {
  name        = "${var.bucket_name}-access"
  description = "Access policy for safehouse bucket"

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

resource "aws_iam_policy_attachment" "safehouse_attach" {
  name       = "${var.bucket_name}-attachment"
  roles      = [var.allowed_role_name]
  policy_arn = aws_iam_policy.safehouse_access.arn
}
