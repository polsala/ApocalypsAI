resource "null_resource" "water_well" {
  triggers = {
    well_name = var.well_name
    capacity  = var.capacity_liters
    threshold = var.alert_threshold
  }

  provisioner "local-exec" {
    command = "echo 'Water well ${var.well_name} initialized with ${var.capacity_liters}L capacity'"
  }
}

output "well_status" {
  value = "Water well ${var.well_name} is operational with ${var.capacity_liters}L capacity"
}

output "remaining_water" {
  value = var.capacity_liters - var.alert_threshold
}
