output "replicated_resource_ids" {
  description = "A list of identifiers for the replicated resources."
  value       = null_resource.replicated_resource[*].triggers.instance_id
}
