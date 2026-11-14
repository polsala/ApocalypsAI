output "log_group_name" {
  description = "The name of the CloudWatch Log Group created."
  value       = aws_cloudwatch_log_group.anomaly_logs.name
}

output "sns_topic_arn" {
  description = "The ARN of the SNS Topic created for notifications."
  value       = aws_sns_topic.anomaly_notifications.arn
}
