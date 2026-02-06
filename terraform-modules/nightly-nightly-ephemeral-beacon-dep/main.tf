resource "aws_s3_bucket" "beacon_bucket" {
  bucket = var.bucket_name
  acl    = "private" # Start with private, then apply public access block and policy

  tags = {
    Name        = "EphemeralBeacon-${var.bucket_name}"
    Environment = "Ephemeral"
    Purpose     = "ApocalypsAI-Beacon"
  }
}

resource "aws_s3_bucket_public_access_block" "beacon_public_access_block" {
  bucket = aws_s3_bucket.beacon_bucket.id

  # These settings allow public access to be granted via bucket policies or object ACLs
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "beacon_bucket_policy" {
  bucket = aws_s3_bucket.beacon_bucket.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid       = "PublicReadGetObject",
        Effect    = "Allow",
        Principal = "*",
        Action    = "s3:GetObject",
        Resource  = "${aws_s3_bucket.beacon_bucket.arn}/*" # Allow public read for all objects in the bucket
      },
    ],
  })
}

resource "aws_s3_bucket_object" "beacon_whisper" {
  bucket       = aws_s3_bucket.beacon_bucket.id
  key          = "whisper.txt"
  content      = var.whisper_content
  content_type = "text/plain"
  acl          = "public-read" # Make the object itself public-read
}
