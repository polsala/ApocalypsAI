output "bucket_id" {
  description = "The ID of the S3 Chrono-Vault bucket."
  value       = aws_s3_bucket.chrono_vault.id
}

output "bucket_arn" {
  description = "The ARN of the S3 Chrono-Vault bucket."
  value       = aws_s3_bucket.chrono_vault.arn
}
