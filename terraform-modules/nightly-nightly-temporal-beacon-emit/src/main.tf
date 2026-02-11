resource "aws_s3_bucket" "temporal_beacon" {
  bucket = "${var.bucket_name_prefix}-${random_id.suffix.hex}"

  tags = {
    Name        = "${var.bucket_name_prefix}-beacon"
    Environment = var.environment
    ManagedBy   = "ApocalypsAI"
  }
}

resource "aws_s3_bucket_versioning" "temporal_beacon_versioning" {
  bucket = aws_s3_bucket.temporal_beacon.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "temporal_beacon_sse" {
  bucket = aws_s3_bucket.temporal_beacon.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "temporal_beacon_public_access" {
  bucket = aws_s3_bucket.temporal_beacon.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "random_id" "suffix" {
  byte_length = 4
}
