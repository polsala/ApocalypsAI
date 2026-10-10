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

provider "random" {}
provider "local" {}

resource "random_pet" "safehouse_name" {
  length    = 2
  separator = "-"
}

resource "local_file" "safehouse_file" {
  filename = "${var.directory}/${random_pet.safehouse_name.id}.txt"
  content  = "Welcome to Safehouse ${random_pet.safehouse_name.id}!"
}
