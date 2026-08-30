resource "aws_s3_bucket" "dust_collector" {
  bucket = "${var.bucket_name_prefix}-cosmic-dust-${random_string.suffix.id}"

  tags = merge(
    var.tags,
    {
      Environment = var.environment
      ManagedBy   = "ApocalypsAI-CosmicDustCollector"
    }
  )
}

resource "aws_s3_bucket_ownership_controls" "dust_collector" {
  bucket = aws_s3_bucket.dust_collector.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "dust_collector" {
  depends_on = [aws_s3_bucket_ownership_controls.dust_collector]
  bucket     = aws_s3_bucket.dust_collector.id
  acl        = "private"
}

resource "aws_cloudwatch_log_group" "dust_logs" {
  name              = "/aws/s3/${aws_s3_bucket.dust_collector.id}-access-logs"
  retention_in_days = 7 # Whimsical default: dust doesn't stick around forever

  tags = merge(
    var.tags,
    {
      Environment = var.environment
      ManagedBy   = "ApocalypsAI-CosmicDustCollector"
    }
  )
}

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}
