resource "aws_s3_bucket" "this" {
  bucket         = var.bucket_name
  force_destroy  = true
  tags = {
    Purpose = "Safehouse"
  }
}

resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket = aws_s3_bucket.this.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "this" {
  bucket = aws_s3_bucket.this.id
  rule {
    id     = "expire-after-30-days"
    status = "Enabled"
    expiration {
      days = 30
    }
    filter {}
  }
}
