output "main_queue_url" {
  description = "The URL of the primary SQS queue."
  value       = aws_sqs_queue.temporal_echo_chamber_queue.id
}

output "dlq_url" {
  description = "The URL of the Dead Letter Queue."
  value       = aws_sqs_queue.temporal_echo_chamber_dlq.id
}

output "archive_bucket_name" {
  description = "The name of the S3 bucket for archiving."
  value       = aws_s3_bucket.temporal_echo_archive_bucket.id
}
