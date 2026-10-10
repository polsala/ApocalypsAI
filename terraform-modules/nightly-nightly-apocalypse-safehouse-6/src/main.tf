terraform {
  required_version = ">= 0.13"
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name
  acl    = "private"

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
    id      = "expire-old-versions"
    enabled = true

    noncurrent_version_expiration {
      days = 30
    }
  }

  tags = {
    Purpose = "Apocalyptic Safehouse"
  }
}

resource "aws_iam_policy" "read_only" {
  name        = "${var.bucket_name}-read-only"
  description = "Read‑only access to the safehouse bucket"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "s3:GetObject",
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
