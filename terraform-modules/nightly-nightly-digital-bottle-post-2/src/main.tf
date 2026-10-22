resource "aws_s3_bucket" "bottle_post_bucket" {
  bucket_prefix = var.bucket_name_prefix
  acl           = var.enable_public_read ? "public-read" : "private" # Configurable public read
  tags          = var.tags

  # Enforce server-side encryption by default
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_s3_bucket_versioning" "bottle_post_versioning" {
  bucket = aws_s3_bucket.bottle_post_bucket.id
  versioning_configuration {
    status = var.versioning_enabled ? "Enabled" : "Suspended"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "bottle_post_lifecycle" {
  bucket = aws_s3_bucket.bottle_post_bucket.id

  rule {
    id     = "expire-old-messages"
    status = "Enabled"

    expiration {
      days = var.message_retention_days
    }
  }
}

# Block public access settings to allow public ACLs/policies if enable_public_read is true
resource "aws_s3_bucket_public_access_block" "bottle_post_public_access_block" {
  bucket = aws_s3_bucket.bottle_post_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# If public read is enabled, ensure the bucket policy allows it
resource "aws_s3_bucket_policy" "bottle_post_policy" {
  count  = var.enable_public_read ? 1 : 0
  bucket = aws_s3_bucket.bottle_post_bucket.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.bottle_post_bucket.arn}/*"
      },
    ]
  })
}

output "bucket_id" {
  description = "The name (ID) of the S3 bucket."
  value       = aws_s3_bucket.bottle_post_bucket.id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.bottle_post_bucket.arn
}

output "bucket_domain_name" {
  description = "The domain name of the S3 bucket."
  value       = aws_s3_bucket.bottle_post_bucket.bucket_domain_name
}
