terraform {
  required_version = \">= 1.0\"
}

provider \"aws\" {
  region = var.region
}

resource \"aws_s3_bucket\" \"this\" {
  bucket = var.bucket_name
  acl    = \"private\"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id      = \"expire-old-objects\"
    enabled = true

    expiration {
      days = 30
    }
  }
}
