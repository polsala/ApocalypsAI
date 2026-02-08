resource "aws_s3_bucket" "beacon_bucket" {
  bucket = var.bucket_name
  acl    = "public-read" # Required for static website hosting

  website {
    index_document = "index.html"
    error_document = "error.html" # Optional, but good practice
  }

  tags = merge(
    var.tags,
    {
      "ManagedBy" = "ApocalypsAI-NightlyCloudBeacon"
      "Purpose"   = "WhimsicalCloudBeacon"
    }
  )
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
        Resource  = "${aws_s3_bucket.beacon_bucket.arn}/*"
      }
    ]
  })
}

resource "aws_s3_bucket_object" "index_html" {
  bucket       = aws_s3_bucket.beacon_bucket.id
  key          = "index.html"
  content_type = "text/html"
  source       = "${path.module}/index.html"
  etag         = filemd5("${path.module}/index.html") # Forces update if content changes
  acl          = "public-read"
}

# Optional: Add an error page
resource "aws_s3_bucket_object" "error_html" {
  bucket       = aws_s3_bucket.beacon_bucket.id
  key          = "error.html"
  content_type = "text/html"
  content      = "<h1>404 - Beacon Lost!</h1><p>The signal is weak, but we persist.</p>"
  acl          = "public-read"
}
