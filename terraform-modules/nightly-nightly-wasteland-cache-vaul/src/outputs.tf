output "bucket_id" {
  description = "The ID of the S3 bucket."
  value       = aws_s3_bucket.cache_vault.id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.cache_vault.arn
}

output "bucket_regional_domain_name" {
  description = "The regional domain name of the S3 bucket."
  value       = aws_s3_bucket.cache_vault.bucket_regional_domain_name
}
