resource "aws_s3_bucket" "chrono_cache" {
  bucket = "${var.bucket_name_prefix}-${random_id.suffix.hex}"

  tags = {
    Name        = "${var.bucket_name_prefix}-chrono-cache"
    ManagedBy   = "ApocalypsAI-ChronoCacheProvisioner"
    Environment = "Ephemeral"
  }
}

resource "aws_s3_bucket_versioning" "chrono_cache_versioning" {
  bucket = aws_s3_bucket.chrono_cache.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "chrono_cache_lifecycle" {
  bucket = aws_s3_bucket.chrono_cache.id

  rule {
    id     = "expire-old-objects"
    status = "Enabled"

    expiration {
      days = var.expiration_days
    }
  }
}

resource "random_id" "suffix" {
  byte_length = 4
}
