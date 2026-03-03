terraform {
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

variable "bucket_name" {
  description = "Name of the safe‑house bucket"
  type        = string
}

resource "null_resource" "bucket_placeholder" {
  triggers = {
    bucket_name = var.bucket_name
  }
}

resource "local_file" "bucket_file" {
  depends_on = [null_resource.bucket_placeholder]
  filename   = "${path.module}/safehouse_${var.bucket_name}.txt"
  content    = "Safehouse bucket ${var.bucket_name} created."
}

output "bucket_path" {
  value = local_file.bucket_file.filename
}
