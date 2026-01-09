terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_sqs_queue" "temporal_echo_chamber_dlq" {
  name                        = "${var.project_name}-${var.environment}-temporal-echo-dlq"
  message_retention_seconds   = 1209600 # 14 days
  visibility_timeout_seconds  = 300
  max_message_size            = 262144 # 256 KB
  delay_seconds               = 0
  receive_wait_time_seconds   = 0

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Purpose     = "TemporalEchoChamberDLQ"
  }
}

resource "aws_sqs_queue" "temporal_echo_chamber_queue" {
  name                        = "${var.project_name}-${var.environment}-temporal-echo-queue"
  message_retention_seconds   = 345600 # 4 days
  visibility_timeout_seconds  = 30
  max_message_size            = 262144 # 256 KB
  delay_seconds               = 0
  receive_wait_time_seconds   = 0

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.temporal_echo_chamber_dlq.arn
    maxReceiveCount     = 5
  })

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Purpose     = "TemporalEchoChamberQueue"
  }
}

resource "aws_s3_bucket" "temporal_echo_archive_bucket" {
  bucket = "${var.project_name}-${var.environment}-temporal-echo-archive-${data.aws_caller_identity.current.account_id}-${var.region}"

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Purpose     = "TemporalEchoArchive"
  }
}

resource "aws_s3_bucket_public_access_block" "temporal_echo_archive_bucket_public_access_block" {
  bucket = aws_s3_bucket.temporal_echo_archive_bucket.id

  block_public_acls       = true
  block_public_and_cross_account_access = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "temporal_echo_archive_bucket_versioning" {
  bucket = aws_s3_bucket.temporal_echo_archive_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Data source to get the AWS account ID for unique S3 bucket naming
data "aws_caller_identity" "current" {}
