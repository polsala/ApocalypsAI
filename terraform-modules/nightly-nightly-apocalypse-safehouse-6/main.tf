terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws    = { source = "hashicorp/aws", version = ">= 5.0" }
    random = { source = "hashicorp/random", version = ">= 3.0" }
  }
}

provider "aws" {
  region                      = var.region
  access_key                  = "FAKEACCESSKEY"
  secret_key                  = "FAKESECRETKEY"
  skip_credentials_validation = true
  skip_requesting_account_id  = true
}

resource "random_password" "bucket_pass" {
  length  = var.password_length
  special = true
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id      = "expire-old-objects"
    enabled = true
    expiration {
      days = var.expiration_days
    }
  }

  tags = {
    "Password" = random_password.bucket_pass.result
    "Purpose"  = "Post‑Apocalyptic Safe‑House"
  }
}
