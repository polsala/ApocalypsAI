resource "aws_s3_bucket" "postbox" {
  bucket_prefix = var.bucket_name_prefix
  tags = merge(var.tags, {
    "ManagedBy" = "ApocalypsAI-NightlyCloudWhispererPostbox"
  })
}

# Required for setting ACLs on new buckets with S3 Object Ownership enabled
resource "aws_s3_bucket_ownership_controls" "postbox_ownership" {
  bucket = aws_s3_bucket.postbox.id
  rule {
    object_ownership = "BucketOwnerPreferred" # Allows ACLs to be used, but bucket owner is preferred
  }
}

resource "aws_s3_bucket_acl" "postbox_acl" {
  depends_on = [aws_s3_bucket_ownership_controls.postbox_ownership]
  bucket = aws_s3_bucket.postbox.id
  acl    = "private" # Ensure the bucket is private by default
}

resource "aws_sns_topic" "whisper_channel" {
  name = var.sns_topic_name
  tags = merge(var.tags, {
    "ManagedBy" = "ApocalypsAI-NightlyCloudWhispererPostbox"
  })
}

resource "aws_sns_topic_policy" "s3_publish_policy" {
  arn    = aws_sns_topic.whisper_channel.arn
  policy = data.aws_iam_policy_document.s3_publish_policy_doc.json
}

data "aws_iam_policy_document" "s3_publish_policy_doc" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["s3.amazonaws.com"]
    }

    actions = [
      "SNS:Publish",
    ]

    resources = [
      aws_sns_topic.whisper_channel.arn,
    ]

    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = [aws_s3_bucket.postbox.arn]
    }
  }
}

resource "aws_s3_bucket_notification" "postbox_notifications" {
  bucket = aws_s3_bucket.postbox.id

  topic {
    topic_arn     = aws_sns_topic.whisper_channel.arn
    events        = ["s3:ObjectCreated:*"]
    filter_prefix = var.notification_filter_prefix
    filter_suffix = var.notification_filter_suffix
  }

  depends_on = [aws_sns_topic_policy.s3_publish_policy]
}
