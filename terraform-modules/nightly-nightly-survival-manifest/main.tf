terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

resource "local_file" "manifest" {
  filename = "${path.module}/manifest.json"
  content  = jsonencode(var.items)
}
