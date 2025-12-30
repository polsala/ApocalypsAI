terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
    null = {
      source  = "hashicorp/null"
      version = ">= 3.0"
    }
  }
}

# Provider configurations
provider "aws" {
  region = var.aws_region
  
  # Only configure if credentials are available
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_region_validation      = true
}

provider "google" {
  project = var.gcp_project
  
  # Only configure if project is set
  skip_provider_registration = var.gcp_project == ""
}

provider "azurerm" {
  subscription_id = var.azure_subscription_id
  
  # Only configure if subscription ID is set
  skip_provider_registration = var.azure_subscription_id == ""
  features {}
}

# Backend configuration (optional)
# terraform {
#   backend "local" {}
# }
