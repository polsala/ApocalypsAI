#############################################
# Nightly Terraform Wasteland Version Requirements
# Ensure compatibility with modern Terraform
#############################################

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
  
  # Backend configuration for state management
  backend "local" {
    # In production, use remote backend like S3
    # with encryption and versioning enabled
  }
}

# Provider configuration
provider "aws" {
  region = var.region
  
  # Enable request/response logging for debugging
  # (Remove in production for security)
  # skip_credentials_validation = false
  # skip_metadata_api_check = false
  # skip_region_validation = false
}

# Configure Terraform to handle large state files
terraform {
  # Limit concurrent operations for stability
  # parallelism = 10
  
  # Enable detailed logging
  # log_level = "INFO"
}

# Configure provider defaults
provider "aws" {
  # Use IAM roles for authentication when possible
  # Assume role configuration can be added here
  
  # Enable retries for transient failures
  max_retries = 5
  
  # Configure timeouts
  default_tags {
    tags = {
      TerraformManaged = "true"
      Project = "ApocalypsAI"
      Module = "Wasteland-Terraform"
      Environment = var.environment
      CreatedBy = "Terraform-Wasteland-Module"
      CreatedAt = formatdate("YYYY-MM-DD", timestamp())
    }
  }
}

# Configure module behavior
terraform {
  # Disable automatic plugin downloads in production
  # disable_checkpoint = true
  
  # Enable detailed plan output
  # required_version = ">= 1.0"
}

# Configure workspace isolation
# terraform {
#   # Use workspaces for environment separation
#   # workspace = "${var.environment}"
# }
