output "s3_bucket_id" {
  description = "The ID of the S3 bucket."
  value       = aws_s3_bucket.stardust_bucket.id
}

output "s3_bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.stardust_bucket.arn
}

output "sns_topic_arn" {
  description = "The ARN of the SNS topic (if enabled)."
  value       = var.enable_notifications ? aws_sns_topic.stardust_notification_topic[0].arn : null
}
