resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}

resource "aws_s3_bucket" "echo_chamber" {
  bucket = "${var.bucket_name_prefix}-${random_string.bucket_suffix.result}"
  acl    = var.acl

  tags = merge(
    var.tags,
    {
      "ManagedBy" = "ApocalypsAI-TemporalEchoChamber"
    }
  )
}

resource "aws_s3_bucket_versioning" "echo_chamber_versioning" {
  bucket = aws_s3_bucket.echo_chamber.id
  versioning_configuration {
    status = "Disabled" # For ephemeral storage, versioning is usually not desired.
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "echo_chamber_lifecycle" {
  bucket = aws_s3_bucket.echo_chamber.id

  rule {
    id     = "expire-old-objects"
    status = "Enabled"

    expiration {
      days = var.expiration_days
    }
  }
}

resource "aws_s3_bucket_public_access_block" "echo_chamber_public_access_block" {
  bucket = aws_s3_bucket.echo_chamber.id

  block_public_acls       = true
  block_public_and_cross_account_access = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
