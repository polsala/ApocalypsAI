output "archive_bucket_name" {
  value       = aws_s3_bucket.critical_archive_bucket.bucket
  description = "The name of the critical ApocalypsAI archive S3 bucket."
}

output "stabilizer_status" {
  value       = null_resource.cloud_config_stabilizer.triggers.drift_check_signal
  description = "The current status signal from the Cloud Configuration Stabilizer."
}
