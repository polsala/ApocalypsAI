output "s3_bucket_arn" {
  description = "The ARN of the secure S3 survival cache bucket."
  value       = aws_s3_bucket.survival_cache.arn
}

output "sns_topic_arn" {
  description = "The ARN of the SNS topic for alerts."
  value       = aws_sns_topic.alert_topic.arn
}

output "cloudwatch_alarm_arn" {
  description = "The ARN of the CloudWatch budget alarm."
  value       = aws_cloudwatch_metric_alarm.budget_alarm.arn
}
