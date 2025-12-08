resource "aws_s3_bucket" "critter_cache" {
  bucket_prefix = var.bucket_name_prefix
  tags = {
    Environment = "ApocalypsAI"
    Purpose     = "CritterComfortCache"
    CritterName = var.critter_name
  }
}

resource "aws_s3_bucket_public_access_block" "critter_cache_block" {
  bucket = aws_s3_bucket.critter_cache.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_object" "comfort_message_object" {
  bucket       = aws_s3_bucket.critter_cache.id
  key          = "comfort_message.txt"
  content      = var.comfort_message
  content_type = "text/plain"
  acl          = "private" # Ensure it's private
}
