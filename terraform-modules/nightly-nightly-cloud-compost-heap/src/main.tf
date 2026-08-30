resource "aws_s3_bucket" "compost_bucket" {
  count  = var.enable_s3_compost_bucket ? 1 : 0
  bucket = "${var.project_name}-compost-heap-${data.aws_caller_identity.current.account_id}-${var.region}"

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-CompostBucket"
    },
  )
}

resource "aws_s3_bucket_public_access_block" "compost_bucket_block" {
  count  = var.enable_s3_compost_bucket ? 1 : 0
  bucket = aws_s3_bucket.compost_bucket[0].id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_sns_topic" "notification_topic" {
  name = "${var.project_name}-CompostNotifications"

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-CompostNotifications"
    },
  )
}

resource "aws_config_rule" "stale_ebs_volume_detector" {
  count = var.enable_ebs_stale_volume_detector ? 1 : 0

  name        = "${var.project_name}-StaleEBSVolumeDetector"
  description = "Detects unattached EBS volumes."
  source {
    owner             = "AWS"
    source_identifier = "EBS_VOLUME_ATTACHMENT_CHECK"
  }

  input_parameters = jsonencode({
    "volumeState" = "available"
  })

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-StaleEBSVolumeDetector"
    },
  )
}

resource "aws_config_rule" "stale_ec2_instance_detector" {
  count = var.enable_ec2_stale_instance_detector ? 1 : 0

  name        = "${var.project_name}-StaleEC2InstanceDetector"
  description = "Detects EC2 instances stopped for more than ${var.stale_instance_age_days} days."
  source {
    owner             = "AWS"
    source_identifier = "EC2_INSTANCE_STOPPED_FOR_LONG_TIME"
  }

  input_parameters = jsonencode({
    "maxStoppedDays" = var.stale_instance_age_days
  })

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-StaleEC2InstanceDetector"
    },
  )
}

data "aws_caller_identity" "current" {}
