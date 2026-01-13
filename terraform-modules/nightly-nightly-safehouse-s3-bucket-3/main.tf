resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id      = "expire-old"
    enabled = true

    expiration {
      days = 365
    }
  }
}

