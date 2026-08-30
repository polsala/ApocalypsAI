output "sqs_queue_arn" {
  description = "The ARN of the SQS queue."
  value       = aws_sqs_queue.whisperwind_queue.arn
}

output "sqs_queue_url" {
  description = "The URL of the SQS queue."
  value       = aws_sqs_queue.whisperwind_queue.id
}

output "sns_topic_arn" {
  description = "The ARN of the SNS topic."
  value       = aws_sns_topic.whisperwind_topic.arn
}
