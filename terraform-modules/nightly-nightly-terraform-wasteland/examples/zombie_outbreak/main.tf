#############################################
# Zombie Outbreak Scenario Configuration
# High security, maximum resources
#############################################

module "zombie_outbreak_survival" {
  source = "../.."
  
  # Environment configuration
  region        = "us-east-1"
  environment   = "zombie-outbreak"
  
  # Enhanced survival resources
  water_tanks   = 15
  food_stores   = 25
  power_generators = 8
  
  # Maximum security measures
  perimeter_fencing = true
  watch_towers  = 12
  security_level = 10
  
  # Communication and monitoring
  radio_towers  = 5
  emergency_frequency = "98.7MHz"
  create_monitoring = true
  enable_logging  = true
  
  # Enhanced backup and recovery
  backup_retention_days = 730
  enable_auto_scaling   = true
  maintenance_window    = "Sun:01:00-Sun:03:00"
  
  # Additional tags for zombie scenario
  resource_tags = {
    ThreatLevel = "ZOMBIE_APOCALYPSE"
    Quarantine  = "ACTIVE"
    Biohazard   = "WARNING"
    LastUpdated = formatdate("YYYY-MM-DD", timestamp())
  }
}

# Output the survival status
output "zombie_outbreak_status" {
  description = "Survival status for zombie outbreak scenario"
  value       = module.zombie_outbreak_survival.survival_status
}

output "zombie_defense_status" {
  description = "Defense readiness for zombie outbreak"
  value = {
    perimeter_integrity = "MAXIMUM"
    watch_tower_coverage = "360_DEGREES"
    emergency_response_time = "2_MINUTES"
    zombie_threat_level = "CONTAINED"
  }
}
