terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0" # Specify a compatible version
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0" # Specify a compatible version
    }
  }
  required_version = ">= 1.0.0"
}
