output "bucket_id" {
  description = "The ID (name) of the Temporal Echo Vault S3 bucket."
  value       = aws_s3_bucket.temporal_echo_vault.id
}

output "bucket_arn" {
  description = "The ARN of the Temporal Echo Vault S3 bucket."
  value       = aws_s3_bucket.temporal_echo_vault.arn
}
