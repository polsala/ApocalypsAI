output "safehouse_name" {
  description = "The generated safehouse name"
  value       = random_pet.safehouse_name.id
}

output "safehouse_path" {
  description = "Full path to the created safehouse file"
  value       = local_file.safehouse_file.filename
}
