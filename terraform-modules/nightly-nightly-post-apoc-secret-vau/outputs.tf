output "password" {
  description = "The generated password"
  value       = random_password.vault.result
  sensitive   = true
}
