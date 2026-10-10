terraform {
  required_version = ">= 1.3.0"

  required_providers {
    aws    = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }
}

provider "aws" {
  # In real usage, configure region and credentials via environment variables.
  # For offline testing we rely on the null backend.
  region = "us-east-1"
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name

  versioning {
    enabled = var.versioning_enabled
  }

  lifecycle_rule {
    id      = "expire-old-objects"
    enabled = true
    expiration {
      days = var.lifecycle_days
    }
  }
}

resource "aws_iam_user" "safehouse_user" {
  name = "${var.bucket_name}-user"
}

resource "aws_iam_user_policy" "s3_access" {
  name = "${var.bucket_name}-policy"
  user = aws_iam_user.safehouse_user.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:*"]
      Resource = [
        aws_s3_bucket.safehouse.arn,
        "${aws_s3_bucket.safehouse.arn}/*"
      ]
    }]
  })
}

resource "aws_iam_access_key" "safehouse_key" {
  user = aws_iam_user.safehouse_user.name
}

output "bucket_id" {
  description = "The ID of the created bucket"
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "The ARN of the created bucket"
  value       = aws_s3_bucket.safehouse.arn
}

output "access_key_id" {
  description = "IAM access key ID for the generated user"
  value       = aws_iam_access_key.safehouse_key.id
}

output "secret_access_key" {
  description = "IAM secret access key (sensitive)"
  value       = aws_iam_access_key.safehouse_key.secret
  sensitive   = true
}
