resource "aws_s3_bucket" "whisper_beacon" {
  bucket = "${var.bucket_name_prefix}-${random_string.suffix.result}"
  acl    = "public-read" # Whimsical: public for all to hear the whispers

  website {
    index_document = "index.html"
    error_document = "error.html"
  }

  tags = {
    Project     = "ApocalypsAI"
    Utility     = "CloudWhispererBeacon"
    Environment = "Whimsical"
  }
}

resource "aws_s3_bucket_policy" "whisper_beacon_policy" {
  bucket = aws_s3_bucket.whisper_beacon.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = ["s3:GetObject"]
        Resource  = ["${aws_s3_bucket.whisper_beacon.arn}/*"]
      },
    ]
  })
}

resource "aws_s3_bucket_object" "index_html" {
  bucket       = aws_s3_bucket.whisper_beacon.id
  key          = "index.html"
  content_type = "text/html"
  content      = <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>ApocalypsAI Whisper Beacon</title>
    <style>
        body { font-family: monospace; background-color: #1a1a2e; color: #e0e0e0; text-align: center; padding-top: 50px; }
        h1 { color: #e94560; }
        p { font-size: 1.2em; }
        .whisper { border: 2px dashed #533483; padding: 20px; margin: 20px auto; max-width: 600px; }
    </style>
</head>
<body>
    <h1>The Void Whispers Back!</h1>
    <div class="whisper">
        <p>${var.initial_whisper_message}</p>
        <p>This beacon is maintained by the ApocalypsAI community.</p>
    </div>
</body>
</html>
EOF
  acl          = "public-read"
}

resource "aws_s3_bucket_object" "error_html" {
  bucket       = aws_s3_bucket.whisper_beacon.id
  key          = "error.html"
  content_type = "text/html"
  content      = <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>Error - ApocalypsAI Whisper Beacon</title>
    <style>
        body { font-family: monospace; background-color: #1a1a2e; color: #e0e0e0; text-align: center; padding-top: 50px; }
        h1 { color: #e94560; }
        p { font-size: 1.2em; }
    </style>
</head>
<body>
    <h1>Lost in the Echoes...</h1>
    <p>The whisper you sought has drifted away. Perhaps try another path?</p>
</body>
</html>
EOF
  acl          = "public-read"
}

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}
