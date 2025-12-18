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

resource "random_pet" "name" {
  length    = 2
  separator = "-"
}

resource "random_id" "id" {
  byte_length = 4
}

resource "null_resource" "radiation_shield" {
  triggers = {
    name = random_pet.name.id
    id   = random_id.id.hex
  }
}
