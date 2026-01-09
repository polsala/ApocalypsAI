output "bucket_name" {
  description = "The bucket name supplied"
  value       = var.bucket_name
}

output "versioning_enabled" {
  description = "Whether versioning is enabled"
  value       = var.versioning_enabled
}

output "encryption_enabled" {
  description = "Whether encryption is enabled"
  value       = var.encryption_enabled
}

output "lifecycle_days" {
  description = "Lifecycle retention period in days"
  value       = var.lifecycle_days
}
