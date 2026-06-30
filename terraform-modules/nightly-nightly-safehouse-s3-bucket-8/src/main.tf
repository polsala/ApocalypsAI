resource "aws_s3_bucket" "this" {
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
    Purpose = "Post‑apocalyptic safe‑house"
  }
}
