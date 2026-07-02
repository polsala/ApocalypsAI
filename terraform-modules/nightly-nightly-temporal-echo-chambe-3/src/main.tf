resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}

resource "aws_s3_bucket" "echo_chamber" {
  bucket = "${var.bucket_name_prefix}-${random_string.suffix.result}"

  tags = {
    Environment = var.environment
    ManagedBy   = "ApocalypsAI-Integrator"
    Utility     = "TemporalEchoChamber"
  }
}

resource "aws_s3_bucket_public_access_block" "echo_chamber_pab" {
  bucket = aws_s3_bucket.echo_chamber.id

  # Whimsical rationale: This module is designed for an "echo chamber"
  # where public access might be desired. These settings allow public
  # access to be granted via bucket policies, rather than blocking it
  # outright. Users should be aware of the implications.
  block_public_acls       = false
  ignore_public_acls      = false
  block_public_policy     = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_lifecycle_configuration" "echo_chamber_lifecycle" {
  bucket = aws_s3_bucket.echo_chamber.id

  rule {
    id     = "expire-old-echoes"
    status = "Enabled"

    expiration {
      days = var.retention_days
    }
  }
}
