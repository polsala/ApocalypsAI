resource "aws_sqs_queue" "whisperwind_queue" {
  name                       = var.queue_name
  delay_seconds              = var.queue_delay_seconds
  max_message_size           = var.queue_max_message_size
  message_retention_seconds  = var.queue_message_retention_seconds
  receive_wait_time_seconds  = var.queue_receive_wait_time_seconds
  visibility_timeout_seconds = var.queue_visibility_timeout_seconds

  tags = merge(var.tags, {
    Name = "${var.queue_name}-whisperwind-queue"
  })
}

resource "aws_sns_topic" "whisperwind_topic" {
  name = var.topic_name
  tags = merge(var.tags, {
    Name = "${var.topic_name}-whisperwind-topic"
  })
}

resource "aws_sns_topic_subscription" "whisperwind_sqs_subscription" {
  topic_arn = aws_sns_topic.whisperwind_topic.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.whisperwind_queue.arn
}

resource "aws_sqs_queue_policy" "whisperwind_queue_policy" {
  queue_url = aws_sqs_queue.whisperwind_queue.id

  policy = jsonencode({
    Version = "2012-10-17",
    Id      = "sqs-policy",
    Statement = [
      {
        Sid       = "AllowSNSToSendMessages",
        Effect    = "Allow",
        Principal = {
          Service = "sns.amazonaws.com"
        },
        Action    = "sqs:SendMessage",
        Resource  = aws_sqs_queue.whisperwind_queue.arn,
        Condition = {
          ArnEquals = {
            "aws:SourceArn" = aws_sns_topic.whisperwind_topic.arn
          }
        }
      }
    ]
  })
}
