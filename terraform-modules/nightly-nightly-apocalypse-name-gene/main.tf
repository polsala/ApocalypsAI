terraform {
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

resource "random_pet" "apoc_name" {
  count     = var.count
  length    = 2
  separator = "-"
  prefix    = "apoc"
}
