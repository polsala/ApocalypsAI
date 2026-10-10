output "bucket_arn" {
  description = "ARN of the created S3 bucket."
  value       = aws_s3_bucket.secret_vault.arn
}

output "secret_arn" {
  description = "ARN of the Secrets Manager secret containing the password."
  value       = aws_secretsmanager_secret.vault_password.arn
}
