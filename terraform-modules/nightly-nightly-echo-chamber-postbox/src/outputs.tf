output "sqs_queue_url" {
  description = "The URL of the created SQS queue."
  value       = aws_sqs_queue.postbox_queue.id
}

output "sns_topic_arn" {
  description = "The ARN of the created SNS topic."
  value       = aws_sns_topic.postbox_topic.arn
}
