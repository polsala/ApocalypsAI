variable "bucket_prefix" {
  type        = string
  default     = "safehouse"
  description = "Prefix for bucket name"
}

variable "tags" {
  type    = map(string)
  default = {}
}

resource "random_pet" "name" {
  length = 2
}

resource "aws_s3_bucket" "this" {
  bucket        = "${var.bucket_prefix}-${random_pet.name.id}"
  force_destroy = true
  tags          = var.tags
}

resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket = aws_s3_bucket.this.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "expire" {
  bucket = aws_s3_bucket.this.id
  rule {
    id     = "expire-noncurrent"
    status = "Enabled"
    noncurrent_version_expiration {
      days = 30
    }
  }
}

output "bucket_id" {
  value = aws_s3_bucket.this.id
}

output "bucket_arn" {
  value = aws_s3_bucket.this.arn
}
