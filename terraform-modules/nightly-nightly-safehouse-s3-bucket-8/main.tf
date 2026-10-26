resource "aws_s3_bucket" "safehouse" {
  bucket         = var.bucket_name
  force_destroy  = true
  tags = {
    Purpose = "Apocalypse Safehouse"
  }
}

resource "aws_s3_bucket_versioning" "safehouse" {
  bucket = aws_s3_bucket.safehouse.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "safehouse" {
  bucket = aws_s3_bucket.safehouse.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "safehouse" {
  bucket = aws_s3_bucket.safehouse.id
  rule {
    id     = "glacier-after-30"
    status = "Enabled"
    transition {
      days          = 30
      storage_class = "GLACIER"
    }
    noncurrent_version_transition {
      days          = 30
      storage_class = "GLACIER"
    }
  }
}
