output "bucket_id" {
  description = "The ID of the created bucket."
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "The ARN of the created bucket."
  value       = aws_s3_bucket.safehouse.arn
}

output "access_password" {
  description = "Randomly generated password for client‑side encryption."
  value       = random_password.access.result
  sensitive   = true
}
