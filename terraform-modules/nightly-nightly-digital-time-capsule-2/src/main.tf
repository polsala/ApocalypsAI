resource "random_id" "bucket_suffix" {
  byte_length = 8
}

resource "aws_s3_bucket" "time_capsule" {
  bucket = "${var.bucket_name_prefix}-${random_id.bucket_suffix.hex}"
  acl    = "private"

  # Enable object lock for immutability
  object_lock_enabled = true

  tags = var.tags
}

resource "aws_s3_bucket_versioning" "time_capsule_versioning" {
  bucket = aws_s3_bucket.time_capsule.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_object_lock_configuration" "time_capsule_object_lock" {
  bucket = aws_s3_bucket.time_capsule.id
  rule {
    default_retention {
      mode  = "GOVERNANCE"
      years = var.retention_years
    }
  }
  # expected_bucket_owner is omitted for simpler offline testing.
  # In a real deployment, it's good practice to include it for explicit ownership.
}

resource "aws_s3_bucket_server_side_encryption_configuration" "time_capsule_encryption" {
  bucket = aws_s3_bucket.time_capsule.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "time_capsule_lifecycle" {
  bucket = aws_s3_bucket.time_capsule.id
  rule {
    id     = "archive_and_expire"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "GLACIER_IR" # Glacier Instant Retrieval
    }

    expiration {
      days = var.retention_years * 365 # Expire after retention_years
    }
  }
}
