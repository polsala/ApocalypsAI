resource "aws_s3_bucket" "bloom_bucket" {
  bucket = "${var.bucket_name_prefix}-ephemeral-cloud-bloom"

  tags = merge(
    var.tags,
    {
      "ManagedBy" = "ApocalypsAI-NightlyEphemeralCloudBloom"
      "Ephemeral" = "true"
    }
  )
}

resource "aws_s3_bucket_acl" "bloom_bucket_acl" {
  # ACLs are required for static website hosting in some configurations.
  # If public access is enabled, we set it to 'public-read'.
  # Otherwise, this resource is not created.
  count  = var.enable_public_access ? 1 : 0
  bucket = aws_s3_bucket.bloom_bucket.id
  acl    = "public-read"
}

resource "aws_s3_bucket_ownership_controls" "bloom_ownership_controls" {
  # Required for ACLs to work with S3 Object Ownership.
  # Must be set to ObjectWriter for public-read ACL.
  count  = var.enable_public_access ? 1 : 0
  bucket = aws_s3_bucket.bloom_bucket.id
  rule {
    object_ownership = "ObjectWriter"
  }
}

resource "aws_s3_bucket_public_access_block" "bloom_public_access_block" {
  # By default, block all public access.
  # If public access is enabled, we disable these blocks.
  bucket = aws_s3_bucket.bloom_bucket.id

  block_public_acls       = !var.enable_public_access
  block_public_policy     = !var.enable_public_access
  ignore_public_acls      = !var.enable_public_access
  restrict_public_buckets = !var.enable_public_access
}

resource "aws_s3_bucket_website_configuration" "bloom_website_config" {
  count  = var.enable_public_access ? 1 : 0
  bucket = aws_s3_bucket.bloom_bucket.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "bloom_lifecycle" {
  bucket = aws_s3_bucket.bloom_bucket.id

  rule {
    id     = "ephemeral-object-expiration"
    status = "Enabled"

    expiration {
      days = var.expiration_days
    }
  }
}
