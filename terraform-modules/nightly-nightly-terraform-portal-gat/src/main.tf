terraform {
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
}

variable "portal_name" {
  description = "Custom portal name"
  type        = string
  default     = ""
}

resource "random_pet" "name" {
  length = 2
}

locals {
  name = var.portal_name != "" ? var.portal_name : random_pet.name.id
}

resource "null_resource" "portal" {
  triggers = {
    portal_name = local.name
  }

  provisioner "local-exec" {
    command = "echo Portal ${local.name} opened at $(date -u +\"%Y-%m-%dT%H:%M:%SZ\")"
  }
}

output "message" {
  value = "Portal ${local.name} is ready."
}
