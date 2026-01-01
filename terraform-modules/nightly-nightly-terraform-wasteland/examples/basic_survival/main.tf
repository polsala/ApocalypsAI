#############################################
# Basic Survival Scenario Configuration
# Minimal setup for getting started
#############################################

module "basic_survival" {
  source = "../.."
  
  # Basic configuration
  region        = "us-east-1"
  environment   = "basic-survival"
  
  # Essential resources
  water_tanks   = 2
  food_stores   = 3
  power_generators = 2
  
  # Basic security
  perimeter_fencing = true
  watch_towers  = 2
  security_level = 5
  
  # Standard communication
  radio_towers  = 2
  emergency_frequency = "101.5MHz"
  create_monitoring = false
  enable_logging  = false
  
  # Standard backup
  backup_retention_days = 365
  enable_auto_scaling   = false
  maintenance_window    = "Sun:02:00-Sun:04:00"
  
  # Basic tags
  resource_tags = {
    ThreatLevel = "LOW"
    LastUpdated = formatdate("YYYY-MM-DD", timestamp())
  }
}

# Output the survival status
output "basic_survival_status" {
  description = "Survival status for basic survival scenario"
  value       = module.basic_survival.survival_status
}

output "basic_survival_summary" {
  description = "Summary of basic survival setup"
  value = {
    water_tanks_deployed = 2
    food_stores_deployed = 3
    power_generators_deployed = 2
    security_towers_deployed = 2
    communication_towers_deployed = 2
    estimated_survival_time = "6-12 months"
  }
}
