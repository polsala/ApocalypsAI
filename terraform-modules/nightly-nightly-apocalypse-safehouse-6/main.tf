terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

resource "local_file" "bucket_config" {
  filename = "${path.module}/${var.bucket_name}.json"
  content  = jsonencode({
    bucket_name      = var.bucket_name,
    versioning       = true,
    encryption       = "AES256",
    lifecycle_days  = var.lifecycle_days
  })
}
