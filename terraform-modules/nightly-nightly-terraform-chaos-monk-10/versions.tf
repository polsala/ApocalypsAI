terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0"
    }
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0"
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

# Provider configurations (examples)
provider "aws" {
  # region = var.aws_region
  # profile = var.aws_profile
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
}

provider "azurerm" {
  # features {}
  skip_provider_registration = true
}

provider "google" {
  # project = var.gcp_project
  # region  = var.gcp_region
  
  # For testing, we skip auth
  skip_credentials_validation = true
  skip_provider_registration  = true
}
