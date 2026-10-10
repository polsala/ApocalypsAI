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

variable "name" {
  description = "Name of the safe‑house"
  type        = string
  default     = "safehouse"
}

resource "random_id" "shelter" {
  byte_length = 4
}

resource "null_resource" "safehouse" {
  triggers = {
    shelter_name = var.name
    shelter_id   = random_id.shelter.hex
  }

  provisioner "local-exec" {
    command = "echo \"Safe‑house '${var.name}' with ID ${random_id.shelter.hex} is ready!\" > ${path.module}/shelter_${random_id.shelter.hex}.txt"
  }
}

output "shelter_id" {
  description = "Random identifier for the safe‑house"
  value       = random_id.shelter.hex
}
