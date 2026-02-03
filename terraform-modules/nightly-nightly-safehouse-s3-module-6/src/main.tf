terraform {
  required_version = ">= 1.3.0"
  required_providers {
    aws    = { source = "hashicorp/aws", version = ">= 4.0" }
    random = { source = "hashicorp/random", version = ">= 3.0" }
  }
}

provider "aws" {
  # The region can be overridden via the AWS_DEFAULT_REGION env var.
  region = var.aws_region
}

resource "random_password" "vault" {
  length           = var.password_length
  special          = var.password_special
  override_characters = "!@#%&*"
}

resource "aws_s3_bucket" "vault" {
  bucket = var.bucket_name
  force_destroy = true

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm     = "AES256"
        # Note: In a real‑world scenario you would use KMS with the generated password.
      }
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "vault_retention" {
  bucket = aws_s3_bucket.vault.id

  rule {
    id     = "expire-old-objects"
    status = "Enabled"

    expiration {
      days = var.retention_days
    }
  }
}

output "bucket_arn" {
  description = "ARN of the created S3 bucket"
  value       = aws_s3_bucket.vault.arn
}

output "generated_password" {
  description = "Random password for the vault (for demonstration purposes)"
  value       = random_password.vault.result
  sensitive   = true
}
