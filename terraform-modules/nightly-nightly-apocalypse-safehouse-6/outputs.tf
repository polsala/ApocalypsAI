output "bucket_arn" {
  description = "ARN of the created S3 bucket"
  value       = aws_s3_bucket.safehouse.arn
}

output "generated_password" {
  description = "Random password attached as a tag"
  value       = random_password.bucket_pass.result
  sensitive   = true
}
