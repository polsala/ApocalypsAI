terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

provider "local" {}

resource "local_file" "supply_files" {
  for_each = { for s in var.supplies : s => s }

  filename = "${path.module}/${var.safehouse_name}/${each.key}.txt"
  content  = "Supply: ${each.key}"
}

resource "local_file" "directory_marker" {
  # Create an empty file to ensure the directory exists
  filename = "${path.module}/${var.safehouse_name}/.keep"
  content  = ""
}
