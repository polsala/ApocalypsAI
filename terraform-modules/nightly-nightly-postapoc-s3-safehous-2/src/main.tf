variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
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

  lifecycle_rule {
    id      = "expire-after-30-days"
    enabled = true

    expiration {
      days = 30
    }
  }

  tags = {
    Purpose = "PostApocSafeHouse"
  }
}

output "bucket_arn" {
  value = aws_s3_bucket.safehouse.arn
}

output "bucket_id" {
  value = aws_s3_bucket.safehouse.id
}
