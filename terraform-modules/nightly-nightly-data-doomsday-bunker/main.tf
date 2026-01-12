resource "aws_s3_bucket" "doomsday_bunker" {
  bucket = "${var.bucket_name_prefix}-${var.environment}-apocalypsai"

  tags = merge(
    {
      Name        = "${var.bucket_name_prefix}-${var.environment}"
      Environment = var.environment
    },
    var.tags
  )
}

resource "aws_s3_bucket_versioning" "doomsday_bunker_versioning" {
  bucket = aws_s3_bucket.doomsday_bunker.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "doomsday_bunker_encryption" {
  bucket = aws_s3_bucket.doomsday_bunker.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "doomsday_bunker_lifecycle" {
  bucket = aws_s3_bucket.doomsday_bunker.id

  rule {
    id     = "archive_old_versions"
    status = "Enabled"

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 3650 # Expire objects after 10 years
    }

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "STANDARD_IA"
    }

    noncurrent_version_expiration {
      noncurrent_days = 365 # Expire noncurrent versions after 1 year
    }
  }
}

resource "aws_s3_bucket_public_access_block" "doomsday_bunker_public_access_block" {
  bucket = aws_s3_bucket.doomsday_bunker.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Optional: Example bucket policy to restrict access to specific IAM roles/users.
# This policy should be customized based on your access requirements.
# Uncomment and modify as needed.
/*
resource "aws_s3_bucket_policy" "doomsday_bunker_policy" {
  bucket = aws_s3_bucket.doomsday_bunker.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = [
            "arn:aws:iam::123456789012:user/apocalypsai-admin",
            "arn:aws:iam::123456789012:role/apocalypsai-recovery-role"
          ]
        }
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.doomsday_bunker.arn,
          "${aws_s3_bucket.doomsday_bunker.arn}/*"
        ]
      },
    ]
  })
}
*/
