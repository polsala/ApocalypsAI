terraform {
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

resource "random_id" "suffix" {
  byte_length = 4
}

resource "local_file" "output" {
  filename = "${var.file_path}-${random_id.suffix.hex}"
  content  = var.content
}
