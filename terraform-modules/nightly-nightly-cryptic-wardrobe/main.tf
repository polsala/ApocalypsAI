resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "wardrobe" {
  bucket = "${var.bucket_name_prefix}-${random_id.suffix.hex}"
  force_destroy = true

  versioning {
    enabled = true
  }

  tags = {
    Purpose = "Secret Wardrobe"
  }
}

resource "aws_s3_bucket_policy" "wardrobe_policy" {
  bucket = aws_s3_bucket.wardrobe.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect    = "Deny",
        Principal = "*",
        Action    = "s3:*",
        Resource  = [
          "${aws_s3_bucket.wardrobe.arn}",
          "${aws_s3_bucket.wardrobe.arn}/*"
        ],
        Condition = {
          Bool = { "aws:SecureTransport" = "false" }
        }
      },
      {
        Effect    = "Allow",
        Principal = {
          AWS = var.allowed_role_arn
        },
        Action    = "s3:*",
        Resource  = [
          "${aws_s3_bucket.wardrobe.arn}",
          "${aws_s3_bucket.wardrobe.arn}/*"
        ]
      }
    ]
  })
}
