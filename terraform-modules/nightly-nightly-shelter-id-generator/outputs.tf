output "shelter_id" {
  description = "The generated random ID"
  value       = random_id.shelter.hex
}

output "shelter_tag" {
  description = "Formatted tag combining name and ID"
  value       = "${var.shelter_name}-${random_id.shelter.hex}"
}
