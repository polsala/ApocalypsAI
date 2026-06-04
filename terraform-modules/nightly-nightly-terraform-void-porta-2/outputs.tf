output "portal_url" {\n  description = "A fabricated URL representing the portal"\n  value       = "https://void.example.com/portal?dest=${var.destination}&time=${var.activation_time}"\n}\n
