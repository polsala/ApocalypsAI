output "safehouse_name" {
  value = random_pet.name.id
}

output "safehouse_id" {
  value = random_id.id.hex
}
