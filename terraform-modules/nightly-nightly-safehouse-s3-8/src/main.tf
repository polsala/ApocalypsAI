resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name
  tags = {
    Purpose = "Post‑Apocalyptic Safehouse"
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
    id     = "expire-old-objects"
    status = "Enabled"
    filter {}
    expiration {
      days = 30
    }
  }
}

resource "aws_s3_bucket_object" "supply" {
  count  = var.create_supply_object ? 1 : 0
  bucket = aws_s3_bucket.safehouse.id
  key    = "supply.txt"
  content = var.supply_content
}
