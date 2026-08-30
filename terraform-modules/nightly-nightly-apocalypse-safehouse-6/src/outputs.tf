output "bucket_id" {
  description = "The ID of the S3 bucket."
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.safehouse.arn
}

output "generated_password" {
  description = "Randomly generated password."
  value       = random_password.safehouse_pwd.result
  sensitive   = true
}
