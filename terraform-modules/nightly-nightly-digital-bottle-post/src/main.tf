resource "aws_s3_bucket" "message_bottle" {
  bucket = var.bucket_name
  acl    = var.public_read ? "public-read" : "private" # Whimsical: public-read by default for broadcasting

  tags = {
    Name        = "DigitalMessageBottle"
    Environment = "ApocalypsAI"
    Purpose     = "Broadcast"
  }
}

resource "aws_s3_bucket_public_access_block" "message_bottle_access_block" {
  count  = var.public_read ? 0 : 1 # Only apply if not public-read
  bucket = aws_s3_bucket.message_bottle.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_object" "initial_message" {
  bucket       = aws_s3_bucket.message_bottle.id
  key          = "initial_message.txt"
  content      = var.message_content
  content_type = "text/plain"
  acl          = var.public_read ? "public-read" : "private" # Whimsical: initial message is public if bucket is
}
