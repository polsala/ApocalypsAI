output "vault_name" {
  description = "The generated, whimsical vault name"
  value       = var.prefix != "" ? "${var.prefix}-${random_pet.vault_name.id}" : random_pet.vault_name.id
}
