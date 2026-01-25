resource "aws_s3_bucket" "pet_rock_bucket" {
  bucket_prefix = var.bucket_name_prefix
  tags = {
    Name        = "CloudPetRock-${var.bucket_name_prefix}"
    Environment = "ApocalypsAI"
    Purpose     = "WhimsicalUtility"
  }
}

resource "aws_s3_bucket_ownership_controls" "pet_rock_bucket_ownership" {
  count  = var.enable_website_hosting ? 1 : 0
  bucket = aws_s3_bucket.pet_rock_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "pet_rock_bucket_public_access_block" {
  bucket = aws_s3_bucket.pet_rock_bucket.id

  block_public_acls       = !var.enable_website_hosting
  block_public_policy     = !var.enable_website_hosting
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_website_configuration" "pet_rock_bucket_website" {
  count  = var.enable_website_hosting ? 1 : 0
  bucket = aws_s3_bucket.pet_rock_bucket.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }

  depends_on = [aws_s3_bucket_ownership_controls.pet_rock_bucket_ownership]
}

resource "aws_s3_bucket_policy" "pet_rock_bucket_policy" {
  count  = var.enable_website_hosting ? 1 : 0
  bucket = aws_s3_bucket.pet_rock_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = ["s3:GetObject"]
        Resource  = ["${aws_s3_bucket.pet_rock_bucket.arn}/*"]
      },
    ]
  })

  depends_on = [
    aws_s3_bucket_website_configuration.pet_rock_bucket_website,
    aws_s3_bucket_public_access_block.pet_rock_bucket_public_access_block
  ]
}

output "bucket_id" {
  description = "The ID of the S3 bucket."
  value       = aws_s3_bucket.pet_rock_bucket.id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.pet_rock_bucket.arn
}

output "website_endpoint" {
  description = "The website endpoint of the S3 bucket if website hosting is enabled."
  value       = var.enable_website_hosting ? aws_s3_bucket_website_configuration.pet_rock_bucket_website[0].website_endpoint : null
}
