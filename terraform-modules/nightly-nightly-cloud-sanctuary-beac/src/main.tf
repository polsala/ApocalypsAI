resource "aws_s3_bucket" "beacon_bucket" {
  bucket = var.create_dns_record ? "${var.subdomain}.${var.domain_name}" : "apocalypsai-beacon-${random_id.bucket_suffix[0].hex}"
  acl    = "public-read" # For static website hosting

  tags = {
    Name        = "ApocalypsAI-Sanctuary-Beacon"
    Environment = "Apocalypse"
  }
}

resource "aws_s3_bucket_website_configuration" "beacon_website" {
  bucket = aws_s3_bucket.beacon_bucket.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_policy" "beacon_bucket_policy" {
  bucket = aws_s3_bucket.beacon_bucket.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Principal = "*",
        Action    = "s3:GetObject",
        Resource  = "${aws_s3_bucket.beacon_bucket.arn}/*",
      },
    ],
  })
}

resource "aws_s3_object" "index_html" {
  bucket       = aws_s3_bucket.beacon_bucket.id
  key          = "index.html"
  content_type = "text/html"
  content = <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ApocalypsAI Sanctuary Beacon</title>
    <style>
        body { font-family: 'Courier New', monospace; background-color: #1a1a1a; color: #00ff00; text-align: center; padding-top: 100px; }
        h1 { font-size: 3em; text-shadow: 0 0 10px #00ff00; }
        p { font-size: 1.5em; }
        .signal { animation: blink 1s infinite; }
        @keyframes blink { 50% { opacity: 0; } }
    </style>
</head>
<body>
    <h1 class="signal">SIGNAL DETECTED</h1>
    <p>--- ApocalypsAI Sanctuary Beacon ---</p>
    <p>${var.beacon_message}</p>
    <p>Stay vigilant. Stay safe.</p>
</body>
</html>
EOF
}

resource "random_id" "bucket_suffix" {
  count       = var.create_dns_record ? 0 : 1
  byte_length = 8
}

data "aws_route53_zone" "selected" {
  count = var.create_dns_record ? 1 : 0
  name  = var.domain_name
  # Mock rationale: This data source will only be evaluated if `create_dns_record` is true.
  # For offline testing, `create_dns_record` is set to false, so this resource is skipped.
  # In a real deployment, this expects an existing Route 53 Hosted Zone for the specified domain_name.
}

resource "aws_route53_record" "beacon_record" {
  count = var.create_dns_record ? 1 : 0

  zone_id = data.aws_route53_zone.selected[0].zone_id
  name    = "${var.subdomain}.${var.domain_name}"
  type    = "A"

  alias {
    name                   = aws_s3_bucket.beacon_bucket.website_endpoint
    zone_id                = aws_s3_bucket.beacon_bucket.hosted_zone_id
    evaluate_target_health = true
  }
}
