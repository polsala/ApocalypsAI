output "bucket_id" {
  description = "The ID of the created bucket"
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "The ARN of the created bucket"
  value       = aws_s3_bucket.safehouse.arn
}

output "access_token" {
  description = "Randomly generated password (sensitive)"
  value       = random_password.access_token.result
  sensitive   = true
}
