output "names" {
  description = "List of generated apocalypse names"
  value       = random_pet.apoc_name[*].id
}
