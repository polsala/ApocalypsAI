resource "aws_s3_bucket" "anomaly_beacon" {
  bucket_prefix = var.bucket_name_prefix
  acl           = "private" # Ensure private by default

  tags = {
    TemporalSignature     = var.temporal_signature
    BeaconFrequency       = var.beacon_frequency
    AnomalyClassification = var.anomaly_classification
    ManagedBy             = "ApocalypsAI-NightlyIntegrator"
  }
}

resource "aws_s3_bucket_versioning" "anomaly_beacon_versioning" {
  bucket = aws_s3_bucket.anomaly_beacon.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "anomaly_beacon_public_access_block" {
  bucket = aws_s3_bucket.anomaly_beacon.id

  block_public_acls             = true
  block_public_and_cross_account_access = true
  ignore_public_acls            = true
  restrict_public_buckets       = true
}

resource "aws_s3_bucket_lifecycle_configuration" "anomaly_beacon_lifecycle" {
  bucket = aws_s3_bucket.anomaly_beacon.id

  rule {
    id     = "archive_and_expire"
    status = "Enabled"

    transition {
      days          = var.archive_days
      storage_class = "GLACIER"
    }

    expiration {
      days = var.expire_days
    }
  }
}
