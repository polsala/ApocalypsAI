resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}

resource "aws_s3_bucket" "message_bottle" {
  bucket = "${var.bucket_name_prefix}-${random_string.bucket_suffix.result}"

  tags = merge(
    var.tags,
    {
      "ManagedBy" = "ApocalypsAI-NightlyIntegrator"
      "Purpose"   = "EphemeralMessageBottle"
    }
  )
}

resource "aws_s3_bucket_acl" "message_bottle_acl" {
  bucket = aws_s3_bucket.message_bottle.id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "message_bottle_versioning" {
  bucket = aws_s3_bucket.message_bottle.id
  versioning_configuration {
    status = "Disabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "message_bottle_encryption" {
  bucket = aws_s3_bucket.message_bottle.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "message_bottle_lifecycle" {
  bucket = aws_s3_bucket.message_bottle.id

  rule {
    id     = "expire_objects"
    status = "Enabled"

    expiration {
      days = var.expiration_days
    }
  }
}

resource "aws_s3_bucket_public_access_block" "message_bottle_public_access_block" {
  bucket = aws_s3_bucket.message_bottle.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
