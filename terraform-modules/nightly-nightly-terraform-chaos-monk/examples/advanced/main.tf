# Advanced chaos monkey configuration

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
  region = "us-west-2"
}

provider "random" {}

# Advanced chaos monkey with multiple environments
module "chaos_monkey_dev" {
  source = "../.."
  
  enable_chaos = true
  chaos_probability = 0.2
  aws_region = "us-west-2"
  target_environment = "development"
  exclusion_tag_key = "Critical"
  exclusion_tag_value = "true"
  chaos_window_start = 10
  chaos_window_end = 16
  max_resources_per_execution = 2
}

module "chaos_monkey_staging" {
  source = "../.."
  
  enable_chaos = true
  chaos_probability = 0.15
  aws_region = "us-west-2"
  target_environment = "staging"
  exclusion_tag_key = "Environment"
  exclusion_tag_value = "production"
  chaos_window_start = 9
  chaos_window_end = 17
  max_resources_per_execution = 1
}

# Multi-region chaos monkey
module "chaos_monkey_eu" {
  source = "../.."
  
  enable_chaos = true
  chaos_probability = 0.1
  aws_region = "eu-west-1"
  target_environment = "testing"
  exclusion_tag_key = "Protected"
  exclusion_tag_value = "yes"
  chaos_window_start = 8
  chaos_window_end = 18
  max_resources_per_execution = 1
}

# Aggregate outputs
output "dev_chaos_report" {
  value       = module.chaos_monkey_dev.chaos_report
  description = "Development environment chaos report"
}

output "staging_chaos_report" {
  value       = module.chaos_monkey_staging.chaos_report
  description = "Staging environment chaos report"
}

output "eu_chaos_report" {
  value       = module.chaos_monkey_eu.chaos_report
  description = "EU region chaos report"
}

output "total_chaos_enabled" {
  value       = module.chaos_monkey_dev.chaos_enabled || 
              module.chaos_monkey_staging.chaos_enabled || 
              module.chaos_monkey_eu.chaos_enabled
  description = "Whether any chaos monkey instances are enabled"
}
