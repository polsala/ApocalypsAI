terraform {
  required_version = ">= 1.0"
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }
}

resource "random_pet" "vault_name" {
  length = 2
}

resource "null_resource" "vault_placeholder" {
  triggers = {
    name = var.prefix != "" ? "${var.prefix}-${random_pet.vault_name.id}" : random_pet.vault_name.id
  }
  provisioner "local-exec" {
    command = "echo 'Vault \"${self.triggers.name}\" created (mock)'
  }
}
