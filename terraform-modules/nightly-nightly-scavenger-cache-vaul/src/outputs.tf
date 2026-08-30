output "s3_bucket_id" {
  description = "The ID of the S3 bucket."
  value       = aws_s3_bucket.cache_vault.id
}

output "s3_bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.cache_vault.arn
}

output "s3_bucket_domain_name" {
  description = "The S3 bucket domain name."
  value       = aws_s3_bucket.cache_vault.bucket_domain_name
}
