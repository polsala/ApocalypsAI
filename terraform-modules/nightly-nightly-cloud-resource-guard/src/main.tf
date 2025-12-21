resource "aws_s3_bucket" "survival_cache" {
  bucket = "${var.project_name}-${var.environment}-survival-cache"

  tags = {
    Name      = "${var.project_name}-${var.environment}-survival-cache"
    Project   = var.project_name
    Environment = var.environment
    ManagedBy = "ApocalypsAI Nightly Integrator"
    Purpose   = "Survival Cache"
  }
}

resource "aws_s3_bucket_public_access_block" "survival_cache_block" {
  bucket_id = aws_s3_bucket.survival_cache.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "survival_cache_versioning" {
  bucket_id = aws_s3_bucket.survival_cache.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "survival_cache_encryption" {
  bucket_id = aws_s3_bucket.survival_cache.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_sns_topic" "alert_topic" {
  name = "${var.project_name}-${var.environment}-alert-topic"

  tags = {
    Name      = "${var.project_name}-${var.environment}-alert-topic"
    Project   = var.project_name
    Environment = var.environment
    ManagedBy = "ApocalypsAI Nightly Integrator"
    Purpose   = "Critical Alerts"
  }
}

resource "aws_cloudwatch_metric_alarm" "budget_alarm" {
  alarm_name          = "${var.project_name}-${var.environment}-budget-alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "EstimatedCharges"
  namespace           = "AWS/Billing"
  period              = "86400" # 1 day
  statistic           = "Maximum"
  threshold           = var.budget_threshold
  alarm_actions       = [aws_sns_topic.alert_topic.arn]

  dimensions = {
    Currency = "USD"
  }

  tags = {
    Name      = "${var.project_name}-${var.environment}-budget-alarm"
    Project   = var.project_name
    Environment = var.environment
    ManagedBy = "ApocalypsAI Nightly Integrator"
    Purpose   = "Cost Monitoring"
  }
}
