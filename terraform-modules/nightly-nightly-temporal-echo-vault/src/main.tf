terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

resource "aws_s3_bucket" "echo_vault" {
  bucket = "${var.bucket_name_prefix}-${random_id.suffix.hex}"
  acl    = "private" # Best practice for private data

  tags = {
    Name        = "${var.bucket_name_prefix}-echo-vault"
    Environment = "ApocalypsAI"
    ManagedBy   = "TemporalEchoVaultModule"
  }
}

resource "random_id" "suffix" {
  byte_length = 8
}

resource "aws_s3_bucket_versioning" "echo_vault_versioning" {
  bucket = aws_s3_bucket.echo_vault.id
  versioning_configuration {
    status = var.enable_versioning ? "Enabled" : "Suspended"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "echo_vault_lifecycle" {
  bucket = aws_s3_bucket.echo_vault.id

  rule {
    id     = "current-version-intelligent-tiering"
    status = "Enabled"

    transition {
      days          = var.echo_chamber_retention_days
      storage_class = "INTELLIGENT_TIERING"
    }

    # Optional: Expire current versions after a very long time if needed
    # expiration {
    #   days = 7300 # 20 years
    # }
  }

  rule {
    id     = "non-current-version-glacier-transition"
    status = "Enabled"

    noncurrent_version_transition {
      days          = var.echo_chamber_glacier_days
      storage_class = "GLACIER"
    }
  }

  rule {
    id     = "non-current-version-decay"
    status = "Enabled"

    noncurrent_version_expiration {
      days = var.echo_chamber_decay_days
    }
  }
}
