terraform {
  required_version = ">= 1.5.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

provider "null" {}

resource "null_resource" "safehouse_bucket" {
  triggers = {
    bucket_name    = var.bucket_name
    versioning     = var.versioning
    encryption     = var.encryption
    retention_days = var.retention_days
  }

  # Mock rationale: This null_resource stands in for an actual aws_s3_bucket.
}
