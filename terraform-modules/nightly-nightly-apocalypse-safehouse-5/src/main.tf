terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

variable "bucket_name" {
  description = "Name of the (mock) S3 bucket"
  type        = string
}

variable "versioning_enabled" {
  description = "Simulated versioning flag"
  type        = bool
  default     = true
}

variable "lifecycle_days" {
  description = "Simulated lifecycle expiration in days"
  type        = number
  default     = 30
}

# Write the bucket name to a local file so we can see the result without any cloud provider
resource "local_file" "bucket_name_file" {
  content  = var.bucket_name
  filename = "${path.module}/bucket_name.txt"
}

# Simulate a lifecycle rule using a null_resource that triggers when inputs change
resource "null_resource" "lifecycle_simulation" {
  triggers = {
    bucket_name       = var.bucket_name
    versioning_enabled = var.versioning_enabled
    lifecycle_days    = var.lifecycle_days
  }

  provisioner "local-exec" {
    command = "echo 'Simulating lifecycle: delete objects after ${var.lifecycle_days} days' > ${path.module}/lifecycle.txt"
  }
}

output "bucket_name" {
  description = "The bucket name passed to the module"
  value       = var.bucket_name
}
