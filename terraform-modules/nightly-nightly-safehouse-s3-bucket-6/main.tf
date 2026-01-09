terraform {
  required_version = ">= 1.0.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
}

provider "null" {}

resource "null_resource" "safehouse_bucket" {
  triggers = {
    bucket_name        = var.bucket_name
    versioning_enabled = var.versioning_enabled
    encryption_enabled = var.encryption_enabled
    lifecycle_days     = var.lifecycle_days
  }
}
