# Production-safe example of chaos monkey usage

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

provider "random" {}

# Production-safe chaos monkey configuration
module "chaos_monkey" {
  source = "../.."
  
  # DISABLED for production - set to true to enable
  enable_chaos = false
  
  # Very low probability for safety
  chaos_probability = 0.01
  
  # Only target specific test environment
  target_environment = "chaos-testing"
  
  # Multiple exclusion criteria
  exclusion_tag_key = "Environment"
  exclusion_tag_value = "production"
  
  # Restrict chaos to weekends only (example)
  chaos_window_start = 0
  chaos_window_end = 23
  
  # Very conservative limit
  max_resources_per_execution = 1
}

# Safety outputs
output "production_safety" {
  value       = "Chaos monkey is DISABLED in production for safety"
  description = "Production safety status"
}

output "chaos_status" {
  value       = module.chaos_monkey.chaos_enabled ? "ENABLED" : "DISABLED"
  description = "Current chaos monkey status"
}
