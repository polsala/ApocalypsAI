output "audit_report" {
  description = "A list of resources found to be missing required tags, including the ARN and the missing tag keys."
  value       = local.missing_tags_resources
}
