#############################################
# Nuclear Winter Scenario Configuration
# Extreme conditions, long-term survival
#############################################

module "nuclear_winter_survival" {
  source = "../.."
  
  # Environment configuration
  region        = "us-west-2"
  environment   = "nuclear-winter"
  
  # Maximum resource capacity for long-term survival
  water_tanks   = 25
  food_stores   = 40
  power_generators = 15
  
  # Enhanced security for resource protection
  perimeter_fencing = true
  watch_towers  = 16
  security_level = 9
  
  # Extended communication range
  radio_towers  = 8
  emergency_frequency = "88.1MHz"
  create_monitoring = true
  enable_logging  = true
  
  # Long-term backup strategy
  backup_retention_days = 1095  # 3 years
  enable_auto_scaling   = true
  maintenance_window    = "Sat:03:00-Sat:05:00"
  
  # Nuclear winter specific tags
  resource_tags = {
    RadiationLevel = "HIGH"
    Temperature   = "EXTREME_COLD"
    DaylightHours = "MINIMAL"
    LastUpdated   = formatdate("YYYY-MM-DD", timestamp())
  }
}

# Output the survival status
output "nuclear_winter_status" {
  description = "Survival status for nuclear winter scenario"
  value       = module.nuclear_winter_survival.survival_status
}

output "nuclear_winter_conditions" {
  description = "Environmental conditions for nuclear winter"
  value = {
    expected_temperature = "-40F to -10F"
    daylight_hours = "2-4 hours per day"
    radiation_level = "ELEVATED"
    survival_duration = "5-10 years"
    resource_efficiency = "MAXIMIZED"
  }
}
