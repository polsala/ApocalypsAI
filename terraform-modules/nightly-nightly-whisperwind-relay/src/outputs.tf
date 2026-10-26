output "sqs_queue_id" {
  description = "The ID of the SQS queue."
  value       = aws_sqs_queue.whisperwind_relay.id
}

output "sqs_queue_arn" {
  description = "The ARN of the SQS queue."
  value       = aws_sqs_queue.whisperwind_relay.arn
}

output "sqs_queue_url" {
  description = "The URL of the SQS queue."
  value       = aws_sqs_queue.whisperwind_relay.url
}
