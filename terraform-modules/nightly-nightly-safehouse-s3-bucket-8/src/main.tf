resource "random_pet" "suffix" {
  length = 2
}

resource "aws_s3_bucket" "this" {
  bucket        = "${var.bucket_name_prefix}-${random_pet.suffix.id}"
  force_destroy = true

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
    id      = "expire-old"
    enabled = true

    expiration {
      days = 30
    }
  }

  tags = var.tags
}
