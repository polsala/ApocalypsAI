terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

resource "aws_s3_bucket" "vault" {
  bucket = "${var.bucket_name_prefix}-${random_string.suffix.result}"

  tags = {
    Name        = "${var.bucket_name_prefix}-apocalypse-vault"
    Environment = "apocalypsai"
  }
}

resource "aws_s3_bucket_versioning" "vault_versioning" {
  bucket = aws_s3_bucket.vault.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "vault_sse" {
  bucket = aws_s3_bucket.vault.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_replication_configuration" "vault_replication" {
  count = var.enable_replication ? 1 : 0

  role   = aws_iam_role.replication_role[0].arn
  bucket = aws_s3_bucket.vault.id

  rule {
    id     = "replicate-all"
    status = "Enabled"
    destination {
      bucket        = var.replication_destination_bucket_arn
      storage_class = "STANDARD"
    }
  }
}

resource "aws_iam_role" "replication_role" {
  count = var.enable_replication ? 1 : 0

  name = "${var.bucket_name_prefix}-s3-replication-role-${random_string.suffix.result}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "s3.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy" "replication_policy" {
  count = var.enable_replication ? 1 : 0

  name = "${var.bucket_name_prefix}-s3-replication-policy-${random_string.suffix.result}"
  role = aws_iam_role.replication_role[0].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetReplicationConfiguration",
          "s3:ListBucket"
        ],
        Effect   = "Allow",
        Resource = [aws_s3_bucket.vault.arn]
      },
      {
        Action = [
          "s3:GetObject",
          "s3:GetObjectVersion",
          "s3:ReplicateObject",
          "s3:ReplicateDelete",
          "s3:ReplicateTags"
        ],
        Effect   = "Allow",
        Resource = ["${aws_s3_bucket.vault.arn}/*"]
      },
      {
        Action = [
          "s3:ReplicateObject",
          "s3:ReplicateDelete",
          "s3:ReplicateTags"
        ],
        Effect   = "Allow",
        Resource = ["${var.replication_destination_bucket_arn}/*"]
      },
      {
        Action = [
          "s3:GetBucketVersioning",
          "s3:PutBucketVersioning"
        ],
        Effect   = "Allow",
        Resource = [var.replication_destination_bucket_arn]
      }
    ]
  })
}

resource "aws_s3_bucket_lifecycle_configuration" "vault_lifecycle" {
  count = var.enable_glacier_archive ? 1 : 0

  bucket = aws_s3_bucket.vault.id

  rule {
    id     = "glacier-transition"
    status = "Enabled"

    transition {
      days          = var.glacier_transition_days
      storage_class = "GLACIER"
    }

    noncurrent_version_transition {
      days          = var.glacier_transition_days
      storage_class = "GLACIER_DEEP_ARCHIVE"
    }

    expiration {
      expired_object_delete_marker = true
    }
  }
}

# Required for unique bucket names
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}
