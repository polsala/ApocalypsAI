output "bucket_id" {
  description = "The ID of the created S3 bucket."
  value       = aws_s3_bucket.dust_collector.id
}

output "bucket_arn" {
  description = "The ARN of the created S3 bucket."
  value       = aws_s3_bucket.dust_collector.arn
}

output "log_group_name" {
  description = "The name of the CloudWatch Log Group for the Cosmic Dust Collector."
  value       = aws_cloudwatch_log_group.dust_logs.name
}
