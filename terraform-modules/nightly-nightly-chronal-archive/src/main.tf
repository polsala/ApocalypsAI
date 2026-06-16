resource "aws_s3_bucket" "chronal_archive" {
  bucket_prefix = var.bucket_name_prefix

  tags = merge(
    {
      "ManagedBy"   = "ApocalypsAI"
      "Environment" = var.environment
      "Purpose"     = "Chronal Archive"
    },
    var.tags
  )
}

resource "aws_s3_bucket_versioning" "chronal_archive_versioning" {
  count  = var.versioning_enabled ? 1 : 0
  bucket = aws_s3_bucket.chronal_archive.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "chronal_archive_encryption" {
  bucket = aws_s3_bucket.chronal_archive.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "chronal_archive_public_access_block" {
  bucket = aws_s3_bucket.chronal_archive.id

  block_public_acls             = true
  block_public_and_cross_account_access = true
  ignore_public_acls            = true
  restrict_public_buckets       = true
}
