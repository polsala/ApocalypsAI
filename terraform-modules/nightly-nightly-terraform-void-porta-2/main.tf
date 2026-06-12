terraform {
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0.0"
    }
    null = {
      source  = "hashicorp/null"
      version = ">= 3.0.0"
    }
  }
}

resource "random_id" "portal_id" {
  byte_length = 8
}

resource "null_resource" "portal" {
  triggers = {
    portal_id   = random_id.portal_id.hex
    portal_name = var.portal_name
  }

  provisioner "local-exec" {
    command = var.greeting != null ? "echo \"${var.greeting} (Portal ID: ${random_id.portal_id.hex})\"" : "echo \"Portal \"${var.portal_name}\" initialized with ID ${random_id.portal_id.hex}\""
  }
}
