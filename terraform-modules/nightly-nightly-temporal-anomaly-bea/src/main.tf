resource "aws_cloudwatch_log_group" "anomaly_logs" {
  name              = "/apocalypsai/${var.project_name}/${var.environment}/temporal-anomalies"
  retention_in_days = 7

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "ApocalypsAI"
  }
}

resource "aws_cloudwatch_metric_filter" "anomaly_metric_filter" {
  name           = "${var.project_name}-${var.environment}-temporal-anomaly-filter"
  pattern        = var.anomaly_pattern
  log_group_name = aws_cloudwatch_log_group.anomaly_logs.name

  metric_transformation {
    name          = "TemporalAnomalyCount"
    namespace     = "ApocalypsAI/TemporalAnomalies"
    value         = "1"
    default_value = "0"
  }
}

resource "aws_sns_topic" "anomaly_notifications" {
  name = "${var.project_name}-${var.environment}-temporal-anomaly-alerts"

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "ApocalypsAI"
  }
}

resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.anomaly_notifications.arn
  protocol  = "email"
  endpoint  = var.notification_email
  # For production, consider adding `confirmation_timeout_in_minutes` and manual confirmation.
  # For this utility, we assume the email will be confirmed by the user.
}

resource "aws_cloudwatch_metric_alarm" "temporal_anomaly_alarm" {
  alarm_name          = "${var.project_name}-${var.environment}-TemporalAnomalyAlarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "TemporalAnomalyCount"
  namespace           = "ApocalypsAI/TemporalAnomalies"
  period              = "60" # 1 minute
  statistic           = "Sum"
  threshold           = var.alarm_threshold
  alarm_description   = "Alarm when temporal anomalies exceed threshold."
  alarm_actions       = [aws_sns_topic.anomaly_notifications.arn]
  ok_actions          = [aws_sns_topic.anomaly_notifications.arn] # Also notify when OK

  dimensions = {
    LogGroupName = aws_cloudwatch_log_group.anomaly_logs.name
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "ApocalypsAI"
  }
}
