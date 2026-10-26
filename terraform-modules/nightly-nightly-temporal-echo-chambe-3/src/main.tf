resource "aws_s3_bucket" "echo_chamber" {
  bucket = var.bucket_name
  acl    = "private" # Best practice

  tags = {
    Environment = "ApocalypsAI"
    Purpose     = "TemporalEchoChamber"
    ManagedBy   = "ApocalypsAI-Integrator"
  }
}

resource "aws_s3_bucket_versioning" "echo_chamber_versioning" {
  bucket = aws_s3_bucket.echo_chamber.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "echo_chamber_lifecycle" {
  bucket = aws_s3_bucket.echo_chamber.id

  rule {
    id     = "echo-fade-rule"
    status = "Enabled"

    noncurrent_version_transition {
      days          = var.retention_days
      storage_class = "GLACIER"
    }

    noncurrent_version_expiration {
      days = var.retention_days + 30 # Expire 30 days after moving to Glacier
    }
  }
}
