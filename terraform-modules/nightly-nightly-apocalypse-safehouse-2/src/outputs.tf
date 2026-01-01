output "bucket_id" {
  description = "ID of the created S3 bucket."
  value       = aws_s3_bucket.safehouse.id
}

output "secret_arn" {
  description = "ARN of the Secrets Manager secret (if created)."
  value       = var.enable_secret ? aws_secretsmanager_secret.access_secret[0].arn : null
}
