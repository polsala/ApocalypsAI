terraform {
  required_version = ">= 1.3.0"

  required_providers {
    random = {
      source  = "hashicorp/random"
      version = ">= 3.5.0"
    }
    local = {
      source  = "hashicorp/local"
      version = ">= 2.4.0"
    }
  }
}

provider "random" {}
provider "local" {}

resource "random_pet" "tree" {
  count  = var.tree_count
  length = 2
}

resource "local_file" "tree_file" {
  count    = var.tree_count
  filename = "${path.module}/trees/tree_${count.index}.txt"
  content  = "Tree ${random_pet.tree[count.index].id} stands tall in the enchanted forest."
}
