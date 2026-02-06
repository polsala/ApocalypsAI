output "bucket_arn" {
  description = "ARN of the created S3 bucket."
  value       = aws_s3_bucket.safehouse.arn
}

output "password_secret_arn" {
  description = "ARN of the Secrets Manager secret containing the random password."
  value       = aws_secretsmanager_secret.access_secret.arn
}
