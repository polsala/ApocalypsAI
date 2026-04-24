resource "aws_s3_bucket" "scavenger_cache" {
  bucket_prefix = var.bucket_name_prefix
  tags          = var.tags

  # Enforce best practices for security and durability
  acl = "private" # Ensure objects are private by default

  # Block all public access
  # This is crucial for security and prevents accidental public exposure
  # of potentially sensitive "scavenged" data.
  # Mock rationale: Ensures the module enforces secure defaults without needing actual AWS interaction.
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "scavenger_cache_versioning" {
  bucket = aws_s3_bucket.scavenger_cache.id
  versioning_configuration {
    status = "Enabled"
  }
  # Mock rationale: Ensures versioning is enabled for data durability, a key feature of the cache.
}

resource "aws_s3_bucket_server_side_encryption_configuration" "scavenger_cache_sse" {
  bucket = aws_s3_bucket.scavenger_cache.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
  # Mock rationale: Ensures data is encrypted at rest, a security best practice for sensitive "scavenged" data.
}
