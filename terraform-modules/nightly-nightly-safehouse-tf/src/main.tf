terraform {
  required_version = ">= 1.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                       = var.region
  skip_credentials_validation = true
  skip_requesting_account_id   = true
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    Purpose = "Apocalypse Safehouse"
  }
}

resource "aws_s3_bucket_policy" "safehouse_policy" {
  bucket = aws_s3_bucket.safehouse.id

  policy = data.aws_iam_policy_document.safehouse_policy.json
}

data "aws_iam_policy_document" "safehouse_policy" {
  statement {
    sid    = "DenyInsecureTransport"
    effect = "Deny"

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions = ["s3:*"]
    resources = [
      "${aws_s3_bucket.safehouse.arn}",
      "${aws_s3_bucket.safehouse.arn}/*"
    ]

    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }
}
