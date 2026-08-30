output "generated_name" {
  description = "The whimsically generated name for the resource."
  value       = local.generated_name
}

output "generated_tags" {
  description = "A map of apocalypse-themed tags for the resource."
  value       = local.common_tags
}
