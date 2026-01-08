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

resource "null_resource" "safehouse" {
  triggers = {
    bucket_name = var.bucket_name
    versioning  = var.versioning
  }

  # Simulate creation with a local-exec that writes a tiny file (no side‑effects)
  provisioner "local-exec" {
    command = "echo \"Mock S3 bucket \${var.bucket_name} created. Versioning: \${var.versioning}\" > .mock_safehouse.txt"
  }
}
