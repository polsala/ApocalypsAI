output "secret_arn" {
  description = "The ARN of the created ephemeral secret."
  value       = aws_secretsmanager_secret.ephemeral_secret.arn
}

output "secret_name" {
  description = "The name of the created ephemeral secret."
  value       = aws_secretsmanager_secret.ephemeral_secret.name
}
