terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

resource "local_file" "safehouse" {
  filename = var.file_path
  content  = var.content
}
