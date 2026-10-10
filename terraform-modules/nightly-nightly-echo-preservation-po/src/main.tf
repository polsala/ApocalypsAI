resource "aws_s3_bucket" "echo_chamber" {
  bucket = "${var.name_prefix}-${var.environment}-${random_string.suffix.result}"
  acl    = "private"

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  lifecycle_rule {
    id = "temporal-decay"

    transition {
      days          = var.retention_days_standard
      storage_class = "GLACIER"
    }

    expiration {
      days = var.retention_days_glacier
    }

    enabled = true
  }

  tags = merge(
    {
      "Name"        = "${var.name_prefix}-${var.environment}"
      "Environment" = var.environment
      "ManagedBy"   = "ApocalypsAI-EchoPreservationPod"
    },
    var.tags
  )
}

resource "aws_s3_bucket_public_access_block" "echo_chamber_block" {
  bucket = aws_s3_bucket.echo_chamber.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}
