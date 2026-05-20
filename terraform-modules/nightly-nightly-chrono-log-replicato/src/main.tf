resource "aws_s3_bucket" "chrono_log_bucket" {
  bucket = var.bucket_name
  acl    = "private" # Best practice

  tags = {
    Name        = var.bucket_name
    Environment = var.environment
    ManagedBy   = "ApocalypsAI-ChronoLogReplicator"
  }
}

resource "aws_s3_bucket_public_access_block" "chrono_log_bucket_public_access_block" {
  bucket = aws_s3_bucket.chrono_log_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_iam_policy" "chrono_log_write_policy" {
  name        = "${var.bucket_name}-write-policy"
  description = "IAM policy for writing chrono-logs to S3 bucket ${var.bucket_name}"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket"
        ],
        Effect   = "Allow",
        Resource = [
          aws_s3_bucket.chrono_log_bucket.arn,
          "${aws_s3_bucket.chrono_log_bucket.arn}/*",
        ],
      },
    ],
  })
}
