terraform {
  required_version = ">= 1.0"
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

provider "random" {}
provider "null" {}
provider "local" {}

resource "random_pet" "name" {
  length = 2
}

resource "null_resource" "safehouse_dir" {
  triggers = {
    name = random_pet.name.id
  }

  provisioner "local-exec" {
    command = "mkdir -p ${path.module}/safehouse_${random_pet.name.id}"
  }
}

resource "local_file" "version_file" {
  depends_on = [null_resource.safehouse_dir]

  filename = "${path.module}/safehouse_${random_pet.name.id}/version.txt"
  content  = var.version
}
