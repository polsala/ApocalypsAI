output "prefix" {
  description = "A standardized naming prefix for resources in this constellation."
  value       = local.generated_prefix
}

output "tags" {
  description = "A map of tags to apply to all resources within this constellation."
  value       = local.merged_tags
}
