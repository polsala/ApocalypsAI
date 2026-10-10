resource "aws_s3_bucket" "anomaly_beacon" {
  bucket_prefix = var.bucket_name_prefix
  tags = {
    Environment = var.environment
    ManagedBy   = "ApocalypsAI-Integrator"
    Utility     = "TemporalAnomalyBeacon"
  }
}

resource "aws_s3_bucket_acl" "anomaly_beacon_acl" {
  bucket = aws_s3_bucket.anomaly_beacon.id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "anomaly_beacon_versioning" {
  bucket = aws_s3_bucket.anomaly_beacon.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "anomaly_beacon_sse" {
  bucket = aws_s3_bucket.anomaly_beacon.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "anomaly_beacon_public_access" {
  bucket = aws_s3_bucket.anomaly_beacon.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "anomaly_beacon_lifecycle" {
  bucket = aws_s3_bucket.anomaly_beacon.id

  rule {
    id     = "temporal-data-retention"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA" # Infrequent Access
    }

    transition {
      days          = 90
      storage_class = "GLACIER" # Archival
    }

    expiration {
      days = 365 # Expire after one year
    }
  }
}
