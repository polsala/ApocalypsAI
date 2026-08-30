terraform {
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

resource "random_password" "vault" {
  length           = var.length
  special          = var.special
  override_special = var.override_special
}
