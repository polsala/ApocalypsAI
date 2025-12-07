terraform {
  required_version = ">= 1.0"
  
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
    null = {
      source  = "hashicorp/null"
      version = ">= 3.0"
    }
    external = {
      source  = "hashicorp/external"
      version = ">= 2.0"
    }
  }
}

# Provider configuration examples (commented out)
# provider "aws" {
#   region = "us-west-2"
# }
# 
# provider "google" {
#   project = "my-project"
#   region  = "us-west1"
# }
# 
# provider "azurerm" {
#   features {}
# }
