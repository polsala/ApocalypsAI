resource "aws_s3_bucket" "postbox" {
  bucket_prefix = var.bucket_name_prefix
  acl           = "private" # Ensures private access by default

  tags = {
    Environment = "ApocalypsAI"
    Utility     = "NightlyWhisperingPostbox"
  }
}

resource "aws_s3_bucket_public_access_block" "postbox_block_public_access" {
  bucket = aws_s3_bucket.postbox.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "postbox_policy" {
  bucket = aws_s3_bucket.postbox.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = "*"
        Action = [
          "s3:PutObject",
          "s3:PutObjectAcl"
        ]
        Resource = "${aws_s3_bucket.postbox.arn}/*"
        Condition = {
          IpAddress = {
            "aws:SourceIp" = var.allowed_ip_cidrs
          }
        }
      },
      {
        Effect = "Deny"
        Principal = "*"
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
          "s3:DeleteObject"
        ]
        Resource = [
          aws_s3_bucket.postbox.arn,
          "${aws_s3_bucket.postbox.arn}/*"
        ]
        Condition = {
          NotIpAddress = {
            "aws:SourceIp" = var.allowed_ip_cidrs
          }
        }
      }
    ]
  })
}
