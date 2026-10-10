resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name
  tags   = var.tags
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
    expiration {
      days = 30
    }
    filter {}
  }
}

resource "aws_dynamodb_table" "supply_cache" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "ItemID"

  attribute {
    name = "ItemID"
    type = "S"
  }

  tags = var.tags
}
