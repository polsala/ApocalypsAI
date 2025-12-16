# Example: Multi-Environment Chaos Garden Setup

provider "aws" {
  region = "us-west-2"
}

# Development Chaos Garden
module "chaos_garden_dev" {
  source = "../.."

  environment = "development"
  region      = "us-west-2"

  chaos_scenarios = [
    "network_latency"
  ]

  max_concurrent_experiments = 1
  experiment_duration        = "10m"
  rollback_enabled          = true

  enable_monitoring = true
  alert_email       = "dev-ops@example.com"

  tags = {
    Environment = "development"
    Team        = "DevOps"
    Project     = "ChaosEngineering"
    Terraform   = "true"
  }
}

# Staging Chaos Garden
module "chaos_garden_staging" {
  source = "../.."

  environment = "staging"
  region      = "us-west-2"

  chaos_scenarios = [
    "network_latency",
    "resource_deletion"
  ]

  max_concurrent_experiments = 2
  experiment_duration        = "20m"
  rollback_enabled          = true

  enable_monitoring = true
  alert_email       = "staging-ops@example.com"

  tags = {
    Environment = "staging"
    Team        = "SRE"
    Project     = "ChaosEngineering"
    Terraform   = "true"
  }
}

# Production Chaos Garden (More conservative)
module "chaos_garden_prod" {
  source = "../.."

  environment = "production"
  region      = "us-west-2"

  chaos_scenarios = [
    "network_latency"
  ]

  max_concurrent_experiments = 1
  experiment_duration        = "5m"
  rollback_enabled          = true

  enable_monitoring = true
  alert_email       = "prod-ops@example.com"

  tags = {
    Environment = "production"
    Team        = "SRE"
    Project     = "ChaosEngineering"
    Terraform   = "true"
  }
}

# Output URLs for all environments
output "chaos_garden_urls" {
  value = {
    development = "https://${module.chaos_garden_dev.chaos_garden_url}"
    staging     = "https://${module.chaos_garden_staging.chaos_garden_url}"
    production  = "https://${module.chaos_garden_prod.chaos_garden_url}"
  }
}

output "experiment_buckets" {
  value = {
    development = module.chaos_garden_dev.experiment_results_bucket
    staging     = module.chaos_garden_staging.experiment_results_bucket
    production  = module.chaos_garden_prod.experiment_results_bucket
  }
}
