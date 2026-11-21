terraform {
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0.0"
    }
    local = {
      source  = "hashicorp/local"
      version = ">= 2.0.0"
    }
  }
}

resource "random_id" "rand" {
  byte_length = var.length
}

resource "local_file" "output" {
  filename = var.filename
  content  = random_id.rand.hex
}
