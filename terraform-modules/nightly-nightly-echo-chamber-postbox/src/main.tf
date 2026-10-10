resource "aws_sqs_queue" "postbox_queue" {
  name                       = "${var.name_prefix}-postbox-queue"
  delay_seconds              = 0
  max_message_size           = 262144 # 256 KB
  message_retention_seconds  = 345600 # 4 days
  receive_wait_time_seconds  = 0
  visibility_timeout_seconds = 30

  tags = {
    Name        = "${var.name_prefix}-postbox-queue"
    Environment = "ApocalypsAI"
  }
}

resource "aws_sns_topic" "postbox_topic" {
  name = "${var.name_prefix}-postbox-topic"

  tags = {
    Name        = "${var.name_prefix}-postbox-topic"
    Environment = "ApocalypsAI"
  }
}

resource "aws_sns_topic_subscription" "postbox_subscription" {
  topic_arn = aws_sns_topic.postbox_topic.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.postbox_queue.arn
  # Raw message delivery ensures the message body is sent directly without SNS metadata wrapping
  raw_message_delivery = true
}

# Policy to allow SNS topic to send messages to the SQS queue
data "aws_iam_policy_document" "sqs_queue_policy" {
  statement {
    effect    = "Allow"
    principals {
      type        = "Service"
      identifiers = ["sns.amazonaws.com"]
    }
    actions   = ["sqs:SendMessage"]
    resources = [aws_sqs_queue.postbox_queue.arn]
    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = [aws_sns_topic.postbox_topic.arn]
    }
  }
}

resource "aws_sqs_queue_policy" "postbox_queue_policy" {
  queue_url = aws_sqs_queue.postbox_queue.id
  policy    = data.aws_iam_policy_document.sqs_queue_policy.json
}
