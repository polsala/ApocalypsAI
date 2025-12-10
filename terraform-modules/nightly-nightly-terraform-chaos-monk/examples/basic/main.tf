# Basic example of chaos monkey usage

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

# Include the chaos monkey module
module "chaos_monkey" {
  source = "../.."
  
  # Enable chaos monkey
  enable_chaos = true
  
  # Set chaos probability to 10%
  chaos_probability = 0.1
  
  # Target staging environment
  target_environment = "staging"
  
  # Exclude production resources
  exclusion_tag_key = "Environment"
  exclusion_tag_value = "production"
  
  # Chaos window: 9 AM to 5 PM
  chaos_window_start = 9
  chaos_window_end = 17
  
  # Limit to 1 resource per execution
  max_resources_per_execution = 1
}

# Output the chaos report
output "chaos_report" {
  value       = module.chaos_monkey.chaos_report
  description = "Chaos monkey execution report"
}
