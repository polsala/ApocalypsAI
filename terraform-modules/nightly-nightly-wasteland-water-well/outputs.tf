output "well_status" {
  description = "Current status of the water well"
  value       = module.water_well.well_status
}

output "remaining_water" {
  description = "Available water liters before alert triggers"
  value       = module.water_well.remaining_water
}
