resource \"aws_s3_bucket\" \"this\" {
  bucket = var.bucket_name
  acl    = \"private\"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id      = \"transition-to-glacier\"
    enabled = true

    transition {
      days          = 30
      storage_class = \"GLACIER\"
    }

    expiration {
      days = 365
    }
  }
}
