#############################################
# Nightly Terraform Wasteland Outputs
# Expose survival infrastructure details
#############################################

output "module_version" {
  description = "Version of the wasteland terraform module"
  value       = "1.0.0"
}

output "deployment_region" {
  description = "AWS region where infrastructure was deployed"
  value       = var.region
}

output "environment_name" {
  description = "Environment name for the survival compound"
  value       = var.environment
}

output "resource_count_summary" {
  description = "Summary of all deployed resources"
  value = {
    total_resources = var.water_tanks + var.food_stores + var.power_generators + var.watch_towers + var.radio_towers + (var.perimeter_fencing ? 1 : 0)
    water_tanks     = var.water_tanks
    food_stores     = var.food_stores
    power_generators = var.power_generators
    watch_towers    = var.watch_towers
    radio_towers    = var.radio_towers
    perimeter_fencing = var.perimeter_fencing ? 1 : 0
  }
}

output "survival_readiness_assessment" {
  description = "Comprehensive survival readiness assessment"
  value = {
    water_security = {
      status = var.water_tanks >= 3 ? "SECURE" : var.water_tanks >= 1 ? "ADEQUATE" : "CRITICAL"
      tanks_deployed = var.water_tanks
      estimated_days = var.water_tanks * 30
    }
    
    food_security = {
      status = var.food_stores >= 5 ? "SECURE" : var.food_stores >= 2 ? "ADEQUATE" : "CRITICAL"
      stores_deployed = var.food_stores
      estimated_months = var.food_stores * 6
    }
    
    power_security = {
      status = var.power_generators >= 3 ? "SECURE" : var.power_generators >= 1 ? "ADEQUATE" : "CRITICAL"
      generators_deployed = var.power_generators
      estimated_hours = var.power_generators * 24
    }
    
    security_level = {
      status = var.perimeter_fencing && var.watch_towers >= 4 ? "FORTIFIED" : var.perimeter_fencing && var.watch_towers >= 2 ? "SECURE" : "VULNERABLE"
      fencing_enabled = var.perimeter_fencing
      watch_towers = var.watch_towers
      security_score = var.perimeter_fencing ? var.watch_towers * 10 : 0
    }
    
    communication_capability = {
      status = var.radio_towers >= 3 ? "EXCELLENT" : var.radio_towers >= 2 ? "GOOD" : "LIMITED"
      towers_deployed = var.radio_towers
      frequency = var.emergency_frequency
      coverage_miles = var.radio_towers * 50
    }
  }
}

output "emergency_procedures" {
  description = "Emergency procedures and contact information"
  value = {
    emergency_frequency = var.emergency_frequency
    communication_towers = local.radio_tower_names
    emergency_contacts = [
      "Survivor Network: ${var.emergency_frequency}",
      "Medical Bay: Available",
      "Command Center: Active",
      "Security HQ: Monitoring"
    ]
    evacuation_routes = [
      "Route Alpha: North Ridge",
      "Route Bravo: East Valley",
      "Route Charlie: South Pass"
    ]
  }
}

output "maintenance_schedule" {
  description = "Recommended maintenance schedule for survival infrastructure"
  value = {
    water_tanks = "Monthly inspection and quarterly cleaning"
    food_stores = "Weekly inventory check and monthly rotation"
    power_generators = "Daily fuel check and weekly maintenance"
    watch_towers = "Hourly surveillance rotation"
    radio_towers = "Daily signal check and weekly maintenance"
    perimeter_fencing = "Daily integrity check and weekly repairs"
    maintenance_window = var.maintenance_window
  }
}

output "survival_tips" {
  description = "Additional survival tips and recommendations"
  value = [
    "Rotate food stores regularly to prevent spoilage",
    "Keep water tanks covered to prevent contamination",
    "Maintain generator fuel supplies at 80% capacity",
    "Conduct daily security perimeter checks",
    "Monitor radio communications hourly",
    "Establish backup communication methods",
    "Train all survivors in emergency procedures",
    "Keep medical supplies well-stocked and organized"
  ]
}

output "infrastructure_health" {
  description = "Current health status of all infrastructure"
  value = {
    overall_status = local.total_survival_score >= 10001 ? "EXCELLENT" : local.total_survival_score >= 5001 ? "GOOD" : local.total_survival_score >= 1001 ? "FAIR" : "CRITICAL"
    survival_score = local.total_survival_score
    last_updated = formatdate("YYYY-MM-DD HH:mm:ss Z", timestamp())
    next_maintenance = "${formatdate("YYYY-MM-DD", timeadd(timestamp(), "168h"))} (${var.maintenance_window})"
  }
}

output "resource_dependencies" {
  description = "Dependencies between survival resources"
  value = {
    power_required_for = [
      "Water purification systems",
      "Food refrigeration",
      "Communication equipment",
      "Security systems"
    ]
    
    water_required_for = [
      "Human consumption",
      "Food preparation",
      "Medical facilities",
      "Hygiene systems"
    ]
    
    food_required_for = [
      "Survivor sustenance",
      "Medical recovery",
      "Workforce productivity",
      "Morale maintenance"
    ]
  }
}

output "disaster_recovery_plan" {
  description = "Disaster recovery and backup procedures"
  value = {
    backup_strategy = "Multi-region replication with 365-day retention"
    recovery_time_objective = "4 hours"
    recovery_point_objective = "1 hour"
    backup_locations = [
      "Primary: ${var.region}",
      "Secondary: ${replace(var.region, "-\\d+$", "-2")}",
      "Tertiary: ${replace(var.region, "-\\d+$", "-3")}"
    ]
    emergency_protocols = [
      "Activate backup power generators",
      "Seal perimeter security",
      "Broadcast emergency frequency",
      "Initiate survivor assembly",
      "Deploy medical teams",
      "Secure critical supplies"
    ]
  }
}
