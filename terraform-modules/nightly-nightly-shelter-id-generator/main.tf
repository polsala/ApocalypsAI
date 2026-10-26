terraform {
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

resource "random_id" "shelter" {
  byte_length = var.id_length
}

resource "null_resource" "shelter_meta" {
  triggers = {
    name     = var.shelter_name
    capacity = tostring(var.capacity)
    id       = random_id.shelter.hex
  }
}
