terraform {
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

resource "random_pet" "name" {
  length = 2
}

locals {
  full_name = var.name_prefix != "" ? "${var.name_prefix}-${random_pet.name.id}" : random_pet.name.id
}
