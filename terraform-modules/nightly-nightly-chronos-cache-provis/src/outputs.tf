output "bucket_id" {
  description = "The ID (name) of the S3 bucket."
  value       = aws_s3_bucket.chronos_cache.id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.chronos_cache.arn
}

output "bucket_domain_name" {
  description = "The S3 bucket regional domain name."
  value       = aws_s3_bucket.chronos_cache.bucket_regional_domain_name
}
