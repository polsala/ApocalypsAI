resource "aws_s3_bucket" "chronos_anchor_bucket" {
  bucket = var.bucket_name
  acl    = "private" # Best practice for new buckets

  tags = {
    Name               = var.bucket_name
    chronos_epoch      = floor(timestamp()) # Unix timestamp in seconds
    chronos_decay_days = var.decay_days
    ManagedBy          = "ApocalypsAI-ChronosAnchor"
  }

  # Enable versioning for better data protection (optional, but good practice)
  versioning {
    enabled = true
  }

  # Server-side encryption (optional, but good practice)
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  # Block public access by default (optional, but good practice)
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
