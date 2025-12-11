terraform {
  required_version = ">= 1.0"
  
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }
}

# Provider configurations
provider "random" {
  # No configuration needed for random provider
}
