resource "aws_sqs_queue" "whisperwind_queue" {
  name                       = var.queue_name
  delay_seconds              = var.queue_delay_seconds
  max_message_size           = var.queue_max_message_size
  message_retention_seconds  = var.queue_message_retention_seconds
  receive_wait_time_seconds  = var.queue_receive_wait_time_seconds
  visibility_timeout_seconds = var.queue_visibility_timeout_seconds
  tags                       = var.tags
}

resource "aws_sns_topic" "whisperwind_topic" {
  name = var.topic_name
  tags = var.tags
}

resource "aws_sns_topic_subscription" "whisperwind_subscription" {
  topic_arn = aws_sns_topic.whisperwind_topic.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.whisperwind_queue.arn
}

resource "aws_sqs_queue_policy" "whisperwind_queue_policy" {
  queue_url = aws_sqs_queue.whisperwind_queue.id

  policy = jsonencode({
    Version = "2012-10-17",
    Id      = "sqs-policy-for-sns-topic",
    Statement = [
      {
        Sid       = "AllowSNSTopicToSendMessage",
        Effect    = "Allow",
        Principal = { "AWS" : "*" },
        Action    = "SQS:SendMessage",
        Resource  = aws_sqs_queue.whisperwind_queue.arn,
        Condition = {
          ArnEquals = { "aws:SourceArn" : aws_sns_topic.whisperwind_topic.arn }
        }
      }
    ]
  })
}

variable "queue_name" {
  description = "The name of the SQS queue."
  type        = string
  default     = "whisperwind-message-queue"
}

variable "topic_name" {
  description = "The name of the SNS topic."
  type        = string
  default     = "whisperwind-message-topic"
}

variable "queue_delay_seconds" {
  description = "The length of time, in seconds, for which the delivery of all messages in the queue is delayed."
  type        = number
  default     = 0
}

variable "queue_max_message_size" {
  description = "The limit of how many bytes a message can contain before Amazon SQS rejects it."
  type        = number
  default     = 262144 # 256 KB
}

variable "queue_message_retention_seconds" {
  description = "The number of seconds Amazon SQS retains a message."
  type        = number
  default     = 345600 # 4 days
}

variable "queue_receive_wait_time_seconds" {
  description = "The length of time, in seconds, for which a ReceiveMessage call will wait for a message to arrive."
  type        = number
  default     = 0
}

variable "queue_visibility_timeout_seconds" {
  description = "The duration (in seconds) that an item is hidden from other consumers after a consumer retrieves it."
  type        = number
  default     = 30
}

variable "tags" {
  description = "A map of tags to assign to the resources."
  type        = map(string)
  default     = {
    Project = "ApocalypsAI"
    Utility = "WhisperwindMessageRelay"
  }
}

output "sqs_queue_url" {
  description = "The URL of the SQS queue."
  value       = aws_sqs_queue.whisperwind_queue.id
}

output "sqs_queue_arn" {
  description = "The ARN of the SQS queue."
  value       = aws_sqs_queue.whisperwind_queue.arn
}

output "sns_topic_arn" {
  description = "The ARN of the SNS topic."
  value       = aws_sns_topic.whisperwind_topic.arn
}
