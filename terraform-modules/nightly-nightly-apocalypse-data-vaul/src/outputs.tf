output "vault_bucket_id" {
  description = "The ID (name) of the created S3 bucket."
  value       = aws_s3_bucket.vault.id
}

output "vault_bucket_arn" {
  description = "The ARN of the created S3 bucket."
  value       = aws_s3_bucket.vault.arn
}
