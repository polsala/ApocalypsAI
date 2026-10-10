resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name
  tags = {
    Name            = var.bucket_name
    supply_cache_id = random_id.cache.hex
  }
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
    id     = "expire-old-supplies"
    status = "Enabled"
    expiration {
      days = 30
    }
  }
}

resource "random_id" "cache" {
  byte_length = 4
}
