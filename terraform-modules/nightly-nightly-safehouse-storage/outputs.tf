output "safehouse_name" {
  description = "Random pet name used for the safehouse directory"
  value       = random_pet.name.id
}

output "safehouse_path" {
  description = "Absolute path to the safehouse directory"
  value       = "${path.module}/safehouse_${random_pet.name.id}"
}
