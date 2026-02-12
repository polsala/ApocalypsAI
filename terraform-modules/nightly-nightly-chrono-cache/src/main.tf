resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}

resource "aws_s3_bucket" "chrono_cache" {
  bucket = "${var.bucket_name_prefix}-${random_string.bucket_suffix.result}"
  acl    = "private"

  versioning {
    enabled = false
  n}

  lifecycle_rule {
    id = "chrono-cache-expiration"

    enabled = true

    expiration {
      days = var.expiration_days
    }
  }

  tags = {
    Name        = "ChronoCacheBucket"
    Environment = "Ephemeral"
    ManagedBy   = "ApocalypsAI"
  }
}
