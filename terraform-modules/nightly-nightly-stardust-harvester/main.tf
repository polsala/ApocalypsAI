resource "aws_s3_bucket" "stardust_bucket" {
  bucket_prefix = var.bucket_prefix
  acl           = "private"

  versioning {
    enabled = var.enable_versioning
  }

  lifecycle_rule {
    id = "stardust_lifecycle"

    enabled = true

    transition {
      days          = var.transition_to_ia_days
      storage_class = "STANDARD_IA"
    }

    expiration {
      days = var.expire_objects_days
    }

    abort_incomplete_multipart_upload_days = var.abort_incomplete_multipart_upload_days
  }

  tags = {
    Name        = "${var.bucket_prefix}-stardust-harvester"
    Environment = var.environment
    ManagedBy   = "ApocalypsAI-NightlyIntegrator"
  }
}

resource "aws_s3_bucket_public_access_block" "stardust_bucket_public_access_block" {
  bucket = aws_s3_bucket.stardust_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_sns_topic" "stardust_notification_topic" {
  count = var.enable_notifications ? 1 : 0
  name  = "${var.bucket_prefix}-stardust-notifications"
  tags = {
    Name        = "${var.bucket_prefix}-stardust-notifications"
    Environment = var.environment
    ManagedBy   = "ApocalypsAI-NightlyIntegrator"
  }
}

resource "aws_s3_bucket_notification" "stardust_bucket_notification" {
  count  = var.enable_notifications ? 1 : 0
  bucket = aws_s3_bucket.stardust_bucket.id

  topic {
    topic_arn     = aws_sns_topic.stardust_notification_topic[0].arn
    events        = ["s3:ObjectCreated:*", "s3:ObjectRemoved:*"]
    filter_prefix = var.notification_filter_prefix
  }
}
