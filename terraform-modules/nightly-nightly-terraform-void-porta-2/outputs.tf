output "portal_id" {
  description = "Randomly generated portal identifier"
  value       = random_id.portal_id.hex
}

output "greeting_message" {
  description = "The greeting that was printed (if any)"
  value       = var.greeting != null ? var.greeting : "Portal ${var.portal_name} initialized"
}
