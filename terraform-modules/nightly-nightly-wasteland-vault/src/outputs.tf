output "bucket_id" {
  description = "The ID (name) of the created S3 bucket."
  value       = aws_s3_bucket.wasteland_vault.id
}

output "bucket_arn" {
  description = "The ARN of the created S3 bucket."
  value       = aws_s3_bucket.wasteland_vault.arn
}

output "bucket_domain_name" {
  description = "The domain name of the created S3 bucket."
  value       = aws_s3_bucket.wasteland_vault.bucket_domain_name
}
